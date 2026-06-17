import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8080/ask")

st.set_page_config(page_title="BoardGame GPT", page_icon="🎲")
st.title("BoardGame GPT")
st.caption("Local RAG over BGG data, rulebooks, and reviews.")

if "history" not in st.session_state:
    st.session_state.history = []

for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input("Ask me about board games..."):
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            r = requests.post(API_URL, json={"question": prompt}, timeout=600).json()
        st.markdown(r["answer"])
        st.caption(f"Route: **{r['path']}**")
        if r["sources"]:
            with st.expander("Sources"):
                for s in r["sources"]:
                    st.json(s)
    st.session_state.history.append(("assistant", r["answer"]))
