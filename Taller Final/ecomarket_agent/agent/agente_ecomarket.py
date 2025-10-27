# agent/agente_ecomarket.py
import os
from typing import Any, Dict

# LangChain agent imports (versión 0.3.4)
try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
    from langchain.tools import Tool
    from langchain.prompts import ChatPromptTemplate
    from langchain.chat_models import ChatOpenAI
except Exception as e:
    raise ImportError(f"Error importando componentes de langchain. Detalle: {e}")

# Importa tus herramientas locales
from tools.herramientas_ecomarket import verificar_elegibilidad_devolucion, generar_etiqueta_devolucion
from rag.rag_system import create_or_load_chromadb, consultar_conocimiento_rag

SYSTEM_PROMPT = """
Eres un asistente de servicio al cliente de EcoMarket, amable y profesional.
Cuando corresponda, usa las herramientas disponibles para procesar una devolución:
- verificar_elegibilidad_devolucion
- generar_etiqueta_devolucion

Si la consulta es sobre políticas o FAQs, consulta la base RAG usando la herramienta consultar_conocimiento_rag.
Responde de forma clara y concisa. Si usas una herramienta, informa brevemente qué hiciste y el resultado.
"""

def initialize_ecomarket_agent(openai_api_key: str, persist_dir: str = "./chroma_db") -> Any:
    """
    Inicializa LLM, RAG y crea el agente. Devuelve un AgentExecutor (si disponible) o un dict fallback.
    """
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

    # 1. Inicializar LLM
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    # 2. Inicializar RAG (si existe)
    rag = create_or_load_chromadb(persist_directory=persist_dir, collection_name="ecomarket_rag_data", openai_api_key=openai_api_key)
    retriever = rag.get("retriever") if isinstance(rag, dict) else None

    # 3. Definir herramientas
    tools = [
        Tool(
            name="verificar_elegibilidad_devolucion",
            func=verificar_elegibilidad_devolucion,
            description="Determina si un producto es elegible para devolución. Requiere id_pedido, sku_producto y motivo. Devuelve JSON."
        ),
        Tool(
            name="generar_etiqueta_devolucion",
            func=generar_etiqueta_devolucion,
            description="Genera una etiqueta de devolución. Requiere id_devolucion y direccion_origen."
        )
    ]

    # Agregar herramienta RAG si existe retriever
    if retriever is not None:
        rag_tool = Tool(
            name="consultar_conocimiento_rag",
            func=lambda q: consultar_conocimiento_rag(q, retriever, llm),
            description="Consulta la base de conocimiento (políticas, FAQs)."
        )
        tools.append(rag_tool)

    # 4. Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    # 5. Crear agente ejecutable
    agent_runnable = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

    # 6. AgentExecutor (si está disponible en tu versión)
    try:
        executor = AgentExecutor(agent=agent_runnable, tools=tools, verbose=True)
        return executor
    except Exception:
        # Fallback: devolvemos el runnable y herramientas para invocación manual
        return {"agent": agent_runnable, "tools": tools, "llm": llm, "retriever": retriever}
