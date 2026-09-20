import os
import tempfile

import streamlit as st

from main import build_rag, ask_question

#PAGE

st.set_page_config(
    page_title="DocuMind",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

#STYLE

st.markdown(
    """
    <style>

    .stApp {
        background: #090a0f;
        color: #f5f5f5;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 3rem;
        padding-bottom: 5rem;
    }

    header {
        background: transparent !important;
    }

    footer {
        display: none;
    }

    section[data-testid="stSidebar"] {
        background: #0d0e13;
        border-right: 1px solid #1d2028;
    }

    h1 {
        font-size: 44px !important;
        font-weight: 700 !important;
        letter-spacing: -1.5px !important;
    }

    h2 {
        font-weight: 650 !important;
    }

    h3 {
        font-weight: 600 !important;
    }

    textarea {
        background: #111319 !important;
        color: #f5f5f5 !important;
        border: 1px solid #292d36 !important;
        border-radius: 12px !important;
        font-size: 15px !important;
    }

    textarea:focus {
        border-color: #555b68 !important;
        box-shadow: none !important;
    }

    .stButton > button {
        width: 100%;
        min-height: 44px;
        border-radius: 10px;
        border: 1px solid #30343d;
        background: #eeeeef;
        color: #090a0f;
        font-weight: 650;
    }

    .stButton > button:hover {
        background: #ffffff;
        border-color: #ffffff;
    }

    [data-testid="stFileUploader"] {
        background: #111319;
        border: 1px solid #22252d;
        border-radius: 10px;
        padding: 8px;
    }

    [data-testid="stExpander"] {
        background: #101218;
        border: 1px solid #20232b;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


#SESSION STATE

if "rag" not in st.session_state:

    st.session_state.rag = None


if "file_id" not in st.session_state:

    st.session_state.file_id = None


if "result" not in st.session_state:

    st.session_state.result = None


#SIDEBAR

with st.sidebar:

    st.title(
        "◈ DocuMind"
    )

    st.caption(
        "Document Intelligence"
    )

    st.divider()

    st.subheader(
        "Document"
    )

    uploaded_file = st.file_uploader(
        "Upload your document",
        type=[
            "pdf",
            "docx",
            "txt",
            "md"
        ]
    )

    st.caption(
        "PDF · DOCX · TXT · Markdown"
    )

    st.divider()

    st.subheader(
        "Pipeline"
    )

    st.write(
        "1. Extract document"
    )

    st.write(
        "2. Create chunks"
    )

    st.write(
        "3. Hybrid retrieval"
    )

    st.write(
        "4. Rerank evidence"
    )

    st.write(
        "5. Generate answer"
    )

    st.write(
        "6. Attach citations"
    )


#DOCUMENT PROCESSING

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    file_id = (
        uploaded_file.name,
        len(file_bytes)
    )


    #NEW DOCUMENT

    if file_id != st.session_state.file_id:

        temp_path = None

        try:

            file_extension = os.path.splitext(
                uploaded_file.name
            )[1]


            #TEMP FILE

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:

                temp_file.write(
                    file_bytes
                )

                temp_path = temp_file.name


            #BUILD RAG

            with st.spinner(
                "Reading document and building search index..."
            ):

                st.session_state.rag = build_rag(
                    temp_path
                )

                st.session_state.file_id = file_id

                st.session_state.result = None


        except Exception as error:

            st.session_state.rag = None

            st.session_state.file_id = None

            st.session_state.result = None

            st.error(
                f"Could not process document: {error}"
            )


        finally:

            if (
                temp_path is not None
                and
                os.path.exists(temp_path)
            ):

                os.remove(
                    temp_path
                )


#MAIN HEADER

st.caption(
    "RAG · SOURCE-TRACEABLE ANSWERS"
)

st.title(
    "Ask your documents."
)

st.write(
    "Search your documents with AI and get answers "
    "grounded in the original source passages."
)


#DOCUMENT STATUS

if st.session_state.rag is None:

    st.divider()

    st.info(
        "Upload a document from the sidebar to start asking questions."
    )

    document_ready = False

else:

    rag = st.session_state.rag

    document_count = len(
        rag["documents"]
    )

    chunk_count = len(
        rag["chunks"]
    )

    st.success(
        f"Document ready · "
        f"{document_count} sections · "
        f"{chunk_count} searchable chunks"
    )

    document_ready = True


#QUESTION

st.divider()

st.subheader(
    "What do you want to know?"
)

query = st.text_area(
    "Question",
    placeholder=(
        "Upload a document first, then ask anything about it..."
    ),
    height=110,
    label_visibility="collapsed",
    disabled=not document_ready
)


#ASK BUTTON

ask = st.button(
    "Ask document →",
    type="primary",
    disabled=not document_ready
)


#ASK QUESTION

if ask:

    if not query.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching document and generating answer..."
        ):

            try:

                result = ask_question(
                    st.session_state.rag,
                    query
                )

                st.session_state.result = result

            except Exception as error:

                st.error(
                    f"Something went wrong: {error}"
                )


#RESULT

if st.session_state.result is not None:

    result = st.session_state.result


    #ANSWER

    st.divider()

    st.subheader(
        "Answer"
    )

    st.write(
        result["answer"]
    )


    #SOURCES

    st.divider()

    st.subheader(
        "Sources"
    )

    citations = result["citations"]


    if citations:

        for number, citation in enumerate(
            citations,
            start=1
        ):

            with st.container(
                border=True
            ):

                source_column, location_column = st.columns(
                    [4, 1]
                )

                with source_column:

                    st.write(
                        f"**{number:02d} · "
                        f"{citation['source']}**"
                    )

                with location_column:

                    st.caption(
                        citation["location"]
                    )

                st.write(
                    citation["text"]
                )


    else:

        st.info(
            "No direct citation was found for this answer."
        )


    #RETRIEVED PASSAGES

    st.divider()

    with st.expander(
        "View retrieved passages"
    ):

        st.caption(
            "These passages were retrieved by the "
            "RAG pipeline before generating the answer."
        )


        for number, chunk in enumerate(
            result["chunks"],
            start=1
        ):

            st.write(
                f"**Passage {number}**"
            )

            st.caption(
                f"{chunk['source']} · "
                f"{chunk['location']}"
            )

            st.write(
                chunk["text"]
            )


            if number < len(
                result["chunks"]
            ):

                st.divider()
