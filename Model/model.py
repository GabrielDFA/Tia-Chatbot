import time
from openai import OpenAI
import streamlit as st
from openai.error import OpenAIError, InvalidRequestError, APIError

api_key = st.secrets["API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]

def load_openai_client_and_assistant():
    client = OpenAI(api_key=api_key)
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create()
    return client, my_assistant, thread

def wait_on_run(client, run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_assistant_response(client, assistant_thread, user_input=""):
    try:
        message = client.beta.threads.messages.create(
            thread_id=assistant_thread.id,
            role="user",
            content=user_input,
        )
        run = client.beta.threads.runs.create(
            thread_id=assistant_thread.id,
            assistant_id=assistant_id,
        )
        run = wait_on_run(client, run, assistant_thread)
        messages = client.beta.threads.messages.list(
            thread_id=assistant_thread.id, order="asc", after=message.id
        )
        
        # Check if messages are present and structured as expected
        if messages.data and messages.data[0].content and messages.data[0].content[0].text:
            return messages.data[0].content[0].text.value
        else:
            return "Maaf, sepertinya materi yang kamu tanyakan tidak ada pada mata kuliah ini."
    except InvalidRequestError as e:
        st.error(f"Invalid request error: {e}")
        return "Terjadi kesalahan pada permintaan. Mohon cek kembali input Anda."
    except APIError as e:
        st.error(f"API error: {e}")
        return "Terjadi kesalahan pada API. Silakan coba lagi nanti."
    except OpenAIError as e:
        st.error(f"OpenAI error: {e}")
        return "Terjadi kesalahan pada server. Silakan coba lagi nanti."
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return "Terjadi kesalahan yang tidak terduga. Silakan coba lagi nanti."
