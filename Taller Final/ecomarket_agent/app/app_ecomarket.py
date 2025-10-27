# app/app_streamlit.py
import os
import streamlit as st
from agent.agente_ecomarket import initialize_ecomarket_agent
from dotenv import load_dotenv

# Cargar .env si existe
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.warning("Por favor proporciona tu OpenAI API key en el campo o en el archivo .env (OPENAI_API_KEY).")
    st.stop()


st.set_page_config(page_title="EcoMarket - Agente Devoluciones", layout="centered")
st.title("EcoMarket — Agente de Devoluciones (RAG + Tools)")


# Inicializar agente (guardado en session_state para persistencia)
if "agent" not in st.session_state:
    with st.spinner("Inicializando agente y RAG... esto puede tardar un poco la primera vez"):
        try:
            agent = initialize_ecomarket_agent(openai_api_key=OPENAI_API_KEY, persist_dir="./chroma_db")
            st.session_state.agent = agent
            st.success("Agente inicializado.")
        except Exception as e:
            st.error(f"Error al inicializar agente: {e}")
            st.stop()

st.subheader("Ingresar consulta")
prompt = st.text_area("Escribe tu consulta aquí", height=180, placeholder="Ej: 'Quiero devolver el producto SKU ABC-001 del pedido 12345 porque vino dañado. ¿Qué pasos debo seguir?'")

if st.button("Enviar"):
    if not prompt.strip():
        st.warning("Escribe algo en la caja de texto antes de enviar.")
    else:
        agent = st.session_state.agent
        st.info("Ejecutando agente...")
        try:
            # Si es AgentExecutor con .run
            if hasattr(agent, "run"):
                result = agent.run(prompt)
                st.subheader("Respuesta del agente")
                st.write(result)
            else:
                # Fallback: el agent_runnable está en agent["agent"]
                runnable = agent.get("agent")
                out = None
                try:
                    out = runnable.run(prompt)
                except Exception:
                    try:
                        out = runnable.invoke({"input": prompt})
                    except Exception:
                        out = runnable({"input": prompt})
                st.subheader("Respuesta del agente (fallback)")
                st.write(out)
        except Exception as e:
            st.error(f"Error ejecutando el agente: {e}")

st.markdown("---")
st.caption("Nota: la primera ejecución puede tardar si se construye la base vectorial (Chroma).")
