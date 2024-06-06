import streamlit as st
from PIL import Image

def initialize_session_state():
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''

def render_ui():
    logo = Image.open("D:\d3if45-npr-chatbot-tia\Asset\logo.png")
    col1, col2 = st.columns([1, 7])
    with col1:
        st.image(logo, width=80)
    with col2:
        st.title("Tanya TIA 👋")

    st.write("TIA - Tel-U Interactive AI")

    st.text_input("Tanya TIA seputar Sistem Basis Data... ", key='query', on_change=submit)

    user_input = st.session_state.user_input

    st.write("You Entered...", user_input)

    return user_input

def render_response(result):
    container_style = """
    <style>
    .response-container {
        max-width: 700px;
        margin: auto;
    }
    </style>
    """
    st.markdown(container_style, unsafe_allow_html=True)
    st.markdown(f'<div class="response-container"><h2>TIA <span style="color: blue;">Menjawab...</span> 🗣️</h2><p>{result}</p></div>', unsafe_allow_html=True)


