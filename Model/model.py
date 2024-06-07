import os
import time
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

api_key = os.getenv("API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

# Tambahkan print statement untuk debugging
print(f"API Key: {api_key[:4]}...{api_key[-4:]}")  # Hanya cetak sebagian untuk keamanan
print(f"Assistant ID: {assistant_id}")

def load_openai_client_and_assistant():
    try:
        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized successfully")
        my_assistant = client.beta.assistants.retrieve(assistant_id)
        print("Assistant retrieved successfully")
        thread = client.beta.threads.create()
        print("Thread created successfully")
        return client, my_assistant, thread
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        raise

def wait_on_run(client, run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_assistant_response(client, assistant_thread, user_input=""):
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
    return messages.data[0].content[0].text.value
