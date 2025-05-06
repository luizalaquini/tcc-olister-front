import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
API_ENDPOINT = os.getenv("API_ENDPOINT")

# Gerar um conversation_id único com o session_state do streamlit
if 'conversation_id' not in st.session_state:
    st.session_state['conversation_id'] = str(uuid.uuid4())

# Configuração da página
st.set_page_config(page_title="OLISTER", layout="centered")

st.title("💬 Olister")

# Inicializa o histórico de chat na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Adiciona a classe "chat-message" ao estilo das mensagens
        #message_class = 'user' if message["role"] == "user" else 'assistant'
        st.markdown(message["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Envia mensagem para a API Flask
    try:
        # Prepara o payload 
        payload = {
            "conversation_id": st.session_state['conversation_id'], # Identificador da conversa
            "messages": st.session_state.messages # Histórico de mensagens terminando com a última fala do usuário
        }
        
        # Debug payload
        print('******************** payload ********************')
        print(payload)

        # Faz a requisição para a API Flask
        request = requests.post(API_ENDPOINT, json=payload)
        request_json = request.json()

        # Debug response 
        print('******************* response ********************')
        print(request_json)

        # Verifica se a resposta é uma lista e extrai o conteúdo da chave "generation"
        if isinstance(request_json, list) and len(request_json) > 0:
            response = request_json[0].get("generation", {}).get("content", "Erro na resposta do servidor.")
        else:
            response = "Formato inesperado da resposta do servidor."

    except requests.exceptions.RequestException as e:
        response = f"Erro ao conectar-se ao servidor. Detalhes: {e}"

    # Exibe a resposta
    with st.chat_message("assistant"):
        st.markdown(response)

    # Adiciona resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})