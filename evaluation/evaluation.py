import json
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from main import build_rag


#SETTINGS

document = r"C:\Users\hp\Downloads\rag_evaluation_50_pages.pdf"

question_file = r"evaluation\questions.json"

k3 = 3

k5 = 5


#LOAD QUESTIONS

with open(
    question_file,
    "r",
    encoding="utf-8"
) as file:

    questions = json.load(file)


#BUILD RAG

rag = build_rag(
    document
)

chunks = rag["chunks"]
model = rag["model"]
reranker = rag["reranker"]
index = rag["index"]
bm25 = rag["bm25"]


#RETRIEVAL

def retrieve(
    query
):

    #QUERY EMBEDDING

    query_embedding = model.encode(
        [query]
    )

    query_embedding = query_embedding.astype(
        "float32"
    )


    #FAISS

    search_k = min(
        5,
        len(chunks)
    )

    distance, indices = index.search(
        query_embedding,
        search_k
    )

    faiss_indices = [
        i
        for i in indices[0].tolist()
        if i >= 0
    ]


    #BM25

    query_tokens = query.lower().split()

    bm25_scores = bm25.get_scores(
        query_tokens
    )

    bm25_indices = sorted(
        range(len(bm25_scores)),
        key=lambda i : bm25_scores[i],
        reverse=True
    )[:search_k]


    #HYBRID

    hybrid_indices = list(
        dict.fromkeys(
            faiss_indices +
            bm25_indices
        )
    )


    retrieved_chunks = [
        chunks[i]
        for i in hybrid_indices
    ]


    #RERANK

    pairs = [
        [
            query,
            chunk["text"]
        ]
        for chunk in retrieved_chunks
    ]

    scores = reranker.predict(
        pairs
    )


    ranked_results = sorted(
        zip(
            scores,
            retrieved_chunks
        ),
        key=lambda x : x[0],
        reverse=True
    )


    #TOP 5

    return [
        chunk
        for score, chunk
        in ranked_results[:k5]
    ]


#EVALUATE

hit3 = 0

hit5 = 0

total = len(
    questions
)


for number, item in enumerate(
    questions,
    start=1
):

    question = item["question"]

    expected_source = item["source"]

    expected_location = item["location"]


    #RETRIEVE

    results = retrieve(
        question
    )


    #CHECK HIT@3

    found3 = False

    for chunk in results[:k3]:

        if (
            chunk["source"] == expected_source
            and
            chunk["location"] == expected_location
        ):

            found3 = True

            break


    #CHECK HIT@5

    found5 = False

    for chunk in results[:k5]:

        if (
            chunk["source"] == expected_source
            and
            chunk["location"] == expected_location
        ):

            found5 = True

            break


    if found3:

        hit3 += 1


    if found5:

        hit5 += 1


    #PRINT

    print(
        f"{number}. {question}"
    )

    print(
        "Expected:",
        expected_source,
        expected_location
    )

    print(
        "Retrieved:"
    )

    for rank, chunk in enumerate(
        results,
        start=1
    ):

        print(
            f"{rank}.",
            chunk["source"],
            chunk["location"]
        )


    print(
        "Hit@3:",
        "PASS" if found3 else "FAIL"
    )

    print(
        "Hit@5:",
        "PASS" if found5 else "FAIL"
    )

    print()


#RESULT

hit3_rate = (
    hit3 / total
) * 100


hit5_rate = (
    hit5 / total
) * 100


print(
    "=============================="
)

print(
    f"Total Questions : {total}"
)

print(
    f"Hit@3 Hits      : {hit3}"
)

print(
    f"Hit@3 Misses    : {total - hit3}"
)

print(
    f"Hit@3           : {hit3_rate:.2f}%"
)

print()

print(
    f"Hit@5 Hits      : {hit5}"
)

print(
    f"Hit@5 Misses    : {total - hit5}"
)

print(
    f"Hit@5           : {hit5_rate:.2f}%"
)

print(
    "=============================="
)