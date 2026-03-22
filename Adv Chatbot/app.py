import streamlit as st
from model import chatbot_response, learn

st.title("🧠 Self-Learning AI Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:")

if user_input:
    response = chatbot_response(user_input)

    if response:
        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("Bot", response))
    else:
        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("Bot", "I don't know. Teach me 👇"))

        new_answer = st.text_input("Your answer:")

        if new_answer:
            msg = learn(user_input, new_answer)
            st.success(msg)

# Display chat
for sender, msg in st.session_state.chat:
    st.write(f"**{sender}:** {msg}")