# Hi! 👋 I’m your Federal Registry Assistant. How can I help you today?

import streamlit as st
import openai
import asyncio
from agent.prompt import SYSTEM_MESSAGE
from agent.llm_model import *
from agent.llm_agent import *  # make sure chat functions are async

client = openai.AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Session state for messages and chat bubbles
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "system", "content": SYSTEM_MESSAGE}
#     ]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "assistant", "content": (
            "Hi! I’m your Federal Registry Assistant.\n\n")}
    ]
    st.session_state.chat_bubbles = [
        ("assistant", 
        "Hi! I’m your Federal Registry Assistant.\n\n")
    ]


if "chat_bubbles" not in st.session_state:
    st.session_state.chat_bubbles = []
if "pending_tasks" not in st.session_state:
    st.session_state.pending_tasks = []


async def chat_with_user(user_input):
    message = await llm_model_call(client, user_input, st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_bubbles.append(("user", user_input))

    if message.tool_calls:
        await tool_call(message, st.session_state.messages)
        final_message = await final_llmcall(client, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": final_message.content})
        st.session_state.chat_bubbles.append(("assistant", final_message.content))
    else:
        st.session_state.messages.append({"role": "assistant", "content": message.content})
        st.session_state.chat_bubbles.append(("assistant", message.content))


# --------- Streamlit UI Starts ----------
st.set_page_config(page_title="Agent Chatbot", page_icon="🤖")
st.title("User Facing chat style RAG Agentic System ")

# Custom Chat Bubble Styles
st.markdown("""
<style>
.chat-message {
    padding: 10px 15px;
    border-radius: 20px;
    margin-bottom: 10px;
    max-width: 80%;
    word-wrap: break-word;
}
.user-message {
    background-color: #dcf8c6;
    margin-left: auto;
    text-align: right;
}
.bot-message {
    background-color: #f1f0f0;
    margin-right: auto;
    text-align: left;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
</style>
""", unsafe_allow_html=True)

# Display Chat Messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, message in st.session_state.chat_bubbles:
    bubble_class = "user-message" if role == "user" else "bot-message"
    st.markdown(f'<div class="chat-message {bubble_class}">{message}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input area
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="user_input", placeholder="Start typing...")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        # Launch the async chat in a background task
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(chat_with_user(user_input))
        loop.run_until_complete(task)
        st.rerun()




