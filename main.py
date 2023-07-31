import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def init():
    # Makes .env available
    load_dotenv()

    # Load the OpenAI-key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="My personal ChatGPT", page_icon="🤖")


def main():
    init()

    # temperature = how random or deterministic the answers should be
    # 0 = same answers if prompt is same, 1 = new answers every time
    chat = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant")
        ]

    st.header("Your personal ChatGPT 🤖")

    with st.sidebar:
        user_input = st.text_input("Your prompt: ", key="user_input")

        # Store promptdata in history
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

    # History of the chat
    messages = st.session_state.get("messages", [])
    # For-loop starting from the second message, [0] = SystemMessage, should not display
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + "_user")
        else:
            message(msg.content, is_user=False, key=str(i) + "_ai")


if __name__ == "__main__":
    main()
