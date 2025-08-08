import re
import random
import streamlit as st

st.set_page_config(page_title="Simple Chat Bot", page_icon="💬")
st.title("💬 Simple Chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "name" not in st.session_state:
    st.session_state.name = None

def normalize(text: str) -> str:
    return re.sub(r"[^a-z\s]", "", text.lower()).strip()

def get_reply(user_text: str) -> str:
    t = normalize(user_text)
    if not t:
        return "Say something :)"

    # learn user's name
    m = re.search(r"\bmy name is ([a-z]+)\b", t)
    if m:
        st.session_state.name = m.group(1).capitalize()
        return f"Nice to meet you, {st.session_state.name}!"

    # greetings
    if re.search(r"\b(hi|hello|hey|yo)\b", t):
        if st.session_state.name:
            return random.choice([f"Hi {st.session_state.name}!", f"Hello {st.session_state.name}!", "Hey!"])
        return random.choice(["Hello!", "Hi!", "Hey!"])

    if "how are you" in t:
        return "I'm good. You?"

    if "your name" in t or "who are you" in t:
        return "I'm a simple web chat bot."

    if "what is my name" in t:
        return st.session_state.name or "I don't know yet. Tell me: 'my name is ...'"

    if re.search(r"\b(bye|quit|exit|goodbye)\b", t):
        return "Goodbye! 👋"

    return random.choice(["Nice.", "Got it.", "Okay.", "Hmm.", "Tell me more."])

with st.sidebar:
    st.header("Controls")
    if st.button("Clear chat"):
        st.session_state.messages.clear()
        st.session_state.name = None
        st.experimental_rerun()
    st.caption("Try: hi, my name is Ravi, how are you, what is my name, bye")

# show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    reply = get_reply(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)