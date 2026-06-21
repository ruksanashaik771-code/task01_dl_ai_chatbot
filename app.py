import streamlit as st
from groq import Groq
from streamlit_option_menu import option_menu
from pypdf import PdfReader
import pandas as pd
import plotly.express as px

# -------------------
# Load Environment
# -------------------
import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# -------------------
# Page Config
# -------------------
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------
# Custom CSS
# -------------------
st.markdown("""
<style>

.stApp{
    background-color:#202123;
}

[data-testid="stSidebar"]{
    background-color:#171717;
}

h1,h2,h3,p,label{
    color:white !important;
}

[data-testid="stChatMessage"]{
    background-color:#2b2d31;
    border-radius:12px;
    padding:10px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------
# Session State
# -------------------
# -------------------
# Session State
# -------------------

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
# -------------------
# Sidebar
# -------------------
from streamlit_option_menu import option_menu

with st.sidebar:

    st.title("🤖 AI Assistant")

    selected = option_menu(
        menu_title=None,
        options=[
            "Chat",
            "PDF Chat",
            "Data Analysis",
            "Resume Analyzer"
        ],
        icons=[
            "chat-dots",
            "file-earmark-pdf",
            "bar-chart",
            "file-person"
        ],
        default_index=0
    )

    st.markdown("---")

    chats = list(
        st.session_state.all_chats.keys()
    )

    selected_chat = st.selectbox(
        "Select Chat",
        chats
    )

    st.session_state.current_chat = selected_chat

    if st.button("➕ New Chat"):

        new_name = (
            f"Chat {len(chats)+1}"
        )

        st.session_state.all_chats[new_name] = []

        st.rerun()
# -------------------
# ==================================
# CHAT PAGE
# ==================================

if selected == "Chat":

    st.title("💬 AI Chat")

    messages = (
        st.session_state
        .all_chats[
            st.session_state.current_chat
        ]
    )

    for message in messages:

        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )

    prompt = st.chat_input(
        "Type your message..."
    )

    if prompt:

        messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        response = (
            client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
        )

        reply = (
            response
            .choices[0]
            .message
            .content
        )

        messages.append(
            {
                "role":"assistant",
                "content":reply
            }
        )

        st.rerun()
# ==================================
# PDF CHAT
# ==================================

if selected == "PDF Chat":

    st.title("📄 PDF Chat")

    pdf = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if pdf:

        reader = PdfReader(pdf)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        question = st.text_input(
            "Ask Question"
        )

        if question:

            response = (
                client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role":"system",
                            "content":text
                        },
                        {
                            "role":"user",
                            "content":question
                        }
                    ]
                )
            )

            st.write(
                response
                .choices[0]
                .message
                .content
            )
# ==================================
# DATA ANALYSIS
# ==================================

if selected == "Data Analysis":

    st.title("📊 Data Analysis")

    file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if file:

        df = pd.read_csv(file)

        st.dataframe(df)

        st.subheader("Statistics")

        st.write(df.describe())

        column = st.selectbox(
            "Select Column",
            df.columns
        )

        fig = px.histogram(
            df,
            x=column
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
# ==================================
# RESUME ANALYZER
# ==================================

if selected == "Resume Analyzer":

    st.title("📄 Resume Analyzer")

    resume = st.file_uploader(
        "Upload Resume",
        type="pdf"
    )

    if resume:

        reader = PdfReader(
            resume
        )

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        response = (
            client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role":"system",
                        "content":
                        """
                        Analyze this resume.

                        Give:
                        ATS Score
                        Skills
                        Missing Skills
                        Suggestions
                        """
                    },
                    {
                        "role":"user",
                        "content":text
                    }
                ]
            )
        )

        st.write(
            response
            .choices[0]
            .message
            .content
        )
