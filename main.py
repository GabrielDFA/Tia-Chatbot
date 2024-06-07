import streamlit as st
from Model.model import load_openai_client_and_assistant, get_assistant_response
from View.view import initialize_session_state, render_ui, render_response

st.set_page_config(page_title="TIA - Tel-U Interactive AI", page_icon=":books:")

try:
    client, my_assistant, assistant_thread = load_openai_client_and_assistant()
except Exception as e:
    st.error(f"Failed to initialize OpenAI client and assistant: {e}")
    st.stop()

initialize_session_state()

user_input = render_ui()

if user_input:
    try:
        result = get_assistant_response(client, assistant_thread, user_input)
        render_response(result)
    except Exception as e:
        st.error(f"Failed to get response from assistant: {e}")
