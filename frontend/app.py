import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8080/ask")

st.set_page_config(page_title="BoardGame GPT", page_icon="🎲")
st.title("BoardGame GPT")
st.caption("RAG sobre dados BGG, rulebooks e reviews.")

if "history" not in st.session_state:
    st.session_state.history = []


def format_source(source: dict) -> str:
    name = source.get("source", "?")
    doc_type = source.get("doc_type", "?")
    game = source.get("game")
    if doc_type == "rulebook":
        label = "Rulebook"
    elif doc_type == "review":
        label = "Review"
    else:
        label = "BGG"
    if game:
        return f"{label}: {name} ({game})"
    return f"{label}: {name}"


def show_sources(sources: list) -> None:
    if not sources:
        return
    unique = []
    seen = set()
    for source in sources:
        key = (source.get("source"), source.get("doc_type"), source.get("game"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(source)
    st.markdown("**Fontes:**")
    for source in unique:
        st.markdown(f"- {format_source(source)}")


for item in st.session_state.history:
    role = item["role"]
    content = item["content"]
    sources = item.get("sources", [])
    with st.chat_message(role):
        st.markdown(content)
        if role == "assistant":
            if item.get("path"):
                st.caption(f"Rota: **{item['path']}**")
            show_sources(sources)

if prompt := st.chat_input("Pergunta sobre jogos de tabuleiro..."):
    st.session_state.history.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("A pensar..."):
            r = requests.post(API_URL, json={"question": prompt}, timeout=600).json()
        st.markdown(r["answer"])
        st.caption(f"Rota: **{r['path']}**")
        show_sources(r.get("sources", []))
    st.session_state.history.append(
        {
            "role": "assistant",
            "content": r["answer"],
            "path": r["path"],
            "sources": r.get("sources", []),
        }
    )
