import streamlit as st
import requests
import json
 
API_BASE = "http://localhost:8080"
 
st.set_page_config(
    page_title="Agente Parecerista ANS – Tester",
    layout="wide"
)
 
st.title("🧠 Agente Parecerista ANS – Test Console")
 
# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
 
def call_get(endpoint: str):
    try:
        resp = requests.get(f"{API_BASE}{endpoint}")
        return resp.status_code, resp.json()
    except Exception as e:
        return 500, {"error": str(e)}
 
def call_post_json(endpoint: str, payload: dict):
    try:
        resp = requests.post(f"{API_BASE}{endpoint}", json=payload)
        return resp.status_code, resp.json()
    except Exception as e:
        return 500, {"error": str(e)}
 
def call_post_file(endpoint: str, file, field_name="file"):
    try:
        file_bytes = file.read()
        resp = requests.post(
            f"{API_BASE}{endpoint}",
            files={field_name: (file.name, file_bytes)}
        )
        return resp.status_code, resp.json()
    except Exception as e:
        return 500, {"error": str(e)}
 
def call_post_form(endpoint: str, texto, files):
    try:
        data = {"texto": texto}
        files_upload = []
 
        if files:
            for f in files:
                files_upload.append(
                    ("files", (f.name, f.read(), f"type"))
                )
 
        resp = requests.post(
            f"{API_BASE}{endpoint}",
            data=data,
            files=files_upload
        )
        return resp.status_code, resp.json()
    except Exception as e:
        return 500, {"error": str(e)}
 
# --------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------
 
with st.sidebar:
    st.header("⚙️ Configurações")
    API_BASE = st.text_input("URL da API", API_BASE)
 
    st.info("Certifique-se que o servidor está rodando: `python server_local.py`")
 
# --------------------------------------------------------------------
# Tabs
# --------------------------------------------------------------------
 
tab_status, tab_health, tab_simples, tab_completo, tab_upload_doc, tab_upload_excel, tab_chat = st.tabs([
    "Status",
    "Health",
    "Parecer Simples",
    "Análise Completa",
    "Upload Documento",
    "Upload Excel",
    "Chat Conversacional"
])
 
# --------------------------------------------------------------------
# STATUS
# --------------------------------------------------------------------
 
with tab_status:
    st.subheader("GET /status")
    if st.button("Consultar Status"):
        code, result = call_get("/status")
        st.write("Status:", code)
        st.json(result)
 
# --------------------------------------------------------------------
# HEALTH
# --------------------------------------------------------------------
 
with tab_health:
    st.subheader("GET /health")
    if st.button("Consultar Health"):
        code, result = call_get("/health")
        st.write("Status:", code)
        st.json(result)
 
# --------------------------------------------------------------------
# PARECER SIMPLES
# --------------------------------------------------------------------
 
with tab_simples:
    st.subheader("POST /consultar_parecer_simples")
 
    texto = st.text_area("Texto de entrada", height=200)
    if st.button("Enviar para análise simples"):
        if texto.strip():
            code, result = call_post_json("/consultar_parecer_simples", {"texto": texto})
            st.write("Status:", code)
            st.json(result)
        else:
            st.warning("Digite um texto antes de enviar.")
 
# --------------------------------------------------------------------
# ANÁLISE COMPLETA (JSON)
# --------------------------------------------------------------------
 
with tab_completo:
    st.subheader("POST /analisar_parecer")
 
    entrada = st.text_area("JSON de entrada", value='{"texto": "Exemplo de parecer"}', height=200)
   
    if st.button("Enviar JSON"):
        try:
            payload = json.loads(entrada)
            code, result = call_post_json("/analisar_parecer", payload)
            st.write("Status:", code)
            st.json(result)
        except json.JSONDecodeError:
            st.error("JSON inválido.")
 
# --------------------------------------------------------------------
# UPLOAD DOCUMENTO PDF / DOCX / TXT
# --------------------------------------------------------------------
 
with tab_upload_doc:
    st.subheader("POST /analisar_documento_parecer")
 
    file = st.file_uploader("Selecione um documento", type=["pdf", "txt", "docx"])
    if file and st.button("Enviar Documento"):
        code, result = call_post_file("/analisar_documento_parecer", file)
        st.write("Status:", code)
        st.json(result)
 
# --------------------------------------------------------------------
# UPLOAD PLANILHA
# --------------------------------------------------------------------
 
with tab_upload_excel:
    st.subheader("POST /analisar_planilha_parecer")
 
    file = st.file_uploader("Selecione uma planilha", type=["xlsx", "xls", "csv"])
    if file and st.button("Enviar Planilha"):
        code, result = call_post_file("/analisar_planilha_parecer", file)
        st.write("Status:", code)
        st.json(result)
 
# --------------------------------------------------------------------
# CHAT CONVERSACIONAL (via /ans_review)
# --------------------------------------------------------------------
 
with tab_chat:
    st.subheader("💬 Chat Conversacional – /ans_review")
 
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
 
    user_input = st.text_area("Digite sua mensagem", height=120)
    files = st.file_uploader("Anexar arquivos (opcional)", type=["pdf", "txt", "png", "jpg", "jpeg", "xlsx"], accept_multiple_files=True)
 
    if st.button("Enviar para o Agente"):
        code, result = call_post_form("/ans_review", user_input, files)
 
        st.session_state.chat_history.append(("Você", user_input))
        st.session_state.chat_history.append(("Agente", result))
 
    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}:**")
        st.json(msg)