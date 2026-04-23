import streamlit as st

from src.chains.response_generator import generate_response

st.title("Civilization 6 Chatbot")
st.write("My name is Monte. How may I help you?")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("You got a question for Monte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prior_messages = st.session_state.messages[:-1]
        answer = generate_response(prompt, prior_messages)

        # answer = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.markdown(answer)
