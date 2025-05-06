# tcc-olister-front

## Run

```bash
streamlit run app.py
```

## Request payload

```python
payload = {
    "conversation_id": st.session_state['conversation_id'], # Identificador da conversa
    "messages": st.session_state.messages # Histórico de mensagens terminando com a última fala do usuário
}
```

## Build and run docker image

**Build:**

``docker build -t olister-front .``

**Run:**

``docker run -p 8501:8501 olister-front``
