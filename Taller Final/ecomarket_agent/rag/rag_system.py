# rag/rag_system.py
import os
import requests
from typing import Optional, Dict, Any, List

# LangChain imports (versión objetivo: langchain==0.3.4)
try:
    from langchain.document_loaders import CSVLoader, PyPDFLoader, JSONLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.schema import Document
except Exception as e:
    raise ImportError(f"Fallo importando LangChain. Asegúrate de instalar las dependencias correctas. Detalle: {e}")

# ---------- Utilidad para descargar archivos desde GitHub raw ----------
def download_file_from_github(raw_url: str, local_filename: str) -> str:
    corrected_url = raw_url.replace("/refs/heads/main/", "/main/")
    print(f"Descargando {local_filename} desde {corrected_url} ...")
    try:
        resp = requests.get(corrected_url, stream=True, timeout=30)
        resp.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Guardado: {local_filename}")
        return local_filename
    except requests.RequestException as ex:
        raise RuntimeError(f"ERROR: No se pudo descargar {local_filename} desde {corrected_url}: {ex}") from ex

# ---------- Creación / carga de documentos (usa el fragmento de tu notebook) ----------
GITHUB_RAW_URL = "https://raw.githubusercontent.com/semurillas/GenIA-20252-ICESI/main/Taller%202/Documentos/"

def load_documents_from_remote(base_url: str = GITHUB_RAW_URL) -> List[Document]:
    """
    Descarga los archivos (CSV, PDFs, JSON) definidos en tu notebook, los carga con los loaders de langchain,
    y devuelve la lista combinada de documentos (sin indexar).
    """
    nro_files = 0
    # CSVs
    pedidos_local = "pedidos_ecomarket.csv"
    inventario_local = "inventario_productos_ecomarket.csv"
    download_file_from_github(base_url + pedidos_local, pedidos_local)
    download_file_from_github(base_url + inventario_local, inventario_local)
    pedidos_docs = CSVLoader(file_path=pedidos_local, encoding="utf-8").load()
    inventario_docs = CSVLoader(file_path=inventario_local, encoding="utf-8").load()
    nro_files += 2

    # PDFs
    devoluciones_local = "Politica_de_Devoluciones_EcoMarket.pdf"
    terminos_local = "Terminos_y_Condiciones_EcoMarket.pdf"
    manual_local = "Manual_de_Uso_Productos_Ecologicos.docx.pdf"
    download_file_from_github(base_url + devoluciones_local, devoluciones_local)
    download_file_from_github(base_url + "Terminos_y_Condiciones_Generales_de_Venta_EcoMarket.pdf", terminos_local)
    download_file_from_github(base_url + manual_local, manual_local)
    devoluciones_docs = PyPDFLoader(devoluciones_local).load_and_split()
    terminos_docs = PyPDFLoader(terminos_local).load_and_split()
    manual_docs = PyPDFLoader(manual_local).load_and_split()
    nro_files += 3

    # JSON FAQ
    faq_local = "faq_ecomarket.json"
    download_file_from_github(base_url + faq_local, faq_local)
    # JSONLoader with jq schema .[] will iterate each element
    faq_docs = JSONLoader(file_path=faq_local, jq_schema=".[]").load()
    nro_files += 1

    print(f"Documentos descargados: {nro_files}")
    # Combine:
    docs_no_split = pedidos_docs + inventario_docs + faq_docs
    docs_to_split = devoluciones_docs + terminos_docs + manual_docs

    # Split PDFs if not already split by loader (we already used load_and_split for PDFs)
    # But apply a text_splitter to enforce chunk sizes (optional)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    pdf_chunks = []
    for d in docs_to_split:
        if hasattr(d, "page_content"):
            chunks = text_splitter.split_documents([d])
            pdf_chunks.extend(chunks)
        else:
            pdf_chunks.append(d)

    final_docs = docs_no_split + pdf_chunks
    print(f"Total final_docs: {len(final_docs)}")
    return final_docs

# ---------- Creación/Carga de Chroma vectorstore ----------
def create_or_load_chromadb(collection_name: str = "ecomarket_rag_data", persist_directory: str = "./chroma_db", openai_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Crea o carga un Chroma vectorstore con OpenAIEmbeddings (persistente en persist_directory).
    Devuelve un dict con keys: vectorstore, retriever, persist_directory.
    """
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory, exist_ok=True)

    # Inicializar embeddings con OpenAI
    embeddings = OpenAIEmbeddings()

    # Si ya existe la carpeta, Chroma.from_existing_collection puede levantarse; la API de Chroma en LangChain permite:
    try:
        vector_db = Chroma(collection_name=collection_name, persist_directory=persist_directory, embedding_function=embeddings)
        # Si la colección está vacía, es posible que necesitemos poblarla afuera
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})
        return {"vectorstore": vector_db, "retriever": retriever, "persist_directory": persist_directory}
    except Exception as e:
        # Intentamos crear y poblar si no existe
        print(f"Intentando crear/poblar Chroma: {e}")
        return {"vectorstore": None, "retriever": None, "persist_directory": persist_directory, "error": str(e)}

def build_rag_from_docs(docs: List[Any], collection_name: str = "ecomarket_rag_data", persist_directory: str = "./chroma_db", openai_api_key: Optional[str] = None):
    """
    Construye/actualiza la base vectorial a partir de final_docs (lista de Document).
    """
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

    embeddings = OpenAIEmbeddings()
    # Create or overwrite vectorstore
    vector_db = Chroma.from_documents(documents=docs, embedding=embeddings, collection_name=collection_name, persist_directory=persist_directory)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    print("ChromaDB creado/poblado con éxito.")
    return {"vectorstore": vector_db, "retriever": retriever, "persist_directory": persist_directory}

# ---------- Consulta RAG ----------
def consultar_conocimiento_rag(query: str, retriever, llm, top_k: int = 3) -> str:
    """
    Ejecuta una búsqueda RAG: obtiene documentos, genera contexto y pide al LLM una respuesta.
    - retriever: objeto con get_relevant_documents(query) o retrieve(query)
    - llm: instancia de ChatOpenAI o similar
    """
    if retriever is None:
        return "RAG no disponible (retriever es None)."

    try:
        docs = retriever.get_relevant_documents(query)
    except Exception:
        try:
            docs = retriever.retrieve(query)
        except Exception as e:
            return f"Error al recuperar documentos: {e}"

    # Formatear contexto
    contexto = ""
    for d in docs:
        metadata = getattr(d, "metadata", {})
        src = metadata.get("source", "")
        content = getattr(d, "page_content", getattr(d, "content", ""))
        contexto += f"Source: {src}\n{content}\n\n"

    prompt = f"""Eres un asistente que usa información de la base de conocimiento para responder. Usa solo la información provista.
Contexto:
{contexto}
Pregunta:
{query}
Respuesta concisa:
"""
    # Invocar LLM robustamente
    try:
        # Prueba: ChatOpenAI tiene varios contratos según versión; intentamos generate -> fallback a __call__
        resp = None
        try:
            resp = llm.generate([{"role": "user", "content": prompt}])
            # extraer texto si la estructura es la habitual
            try:
                texto = resp.generations[0][0].text
            except Exception:
                texto = str(resp)
        except Exception:
            # fallback
            try:
                out = llm(prompt)  # algunos wrappers aceptan string directo
                texto = out.get("text") if isinstance(out, dict) else str(out)
            except Exception:
                try:
                    texto = llm.predict(prompt)
                except Exception as e:
                    texto = f"Error al invocar LLM: {e}"
        return texto
    except Exception as e:
        return f"Error invocando LLM: {e}"
