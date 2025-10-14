<h1> <img width="207" height="112" alt="image" src="https://github.com/user-attachments/assets/89fd906b-04fb-4d4f-b5e6-8375083a8a01" /></h1>
<h1>📚 Maestría en Inteligencia Artificial Aplicada – 3er Semestre</h1>

<h3>Asignatura: Inteligencia Artificial Generativa</h3>

<h3>Taller Práctico Nro. 2 </h3>

<hr style="width:60%;">

<h3>👨‍🎓 Estudiantes</h3>
<ul style="list-style:none; padding:0; font-size:18px;">
    <li>Sebastián Murillas</li>
    <li>Octavio Guerra</li>
</ul>

<hr style="width:60%;">

<h3>📅 Fecha: Octubre 13, 2025</h3>

## 📂 Estructura del Repositorio

| Archivo / Carpeta | Tipo | Descripción |
|--------------------|------|-------------|
| `Taller 2/Documentos/Manual_de_Uso_Productos_Ecologicos.pdf` | PDF | Documento ejemplo de Manuales de Uso de Productos de la compañia EcoMarket |
| `Taller 2/Documentos/Politica_de_Devoluciones_EcoMarket.pdf` | PDF | Documento ejemplo de Políticas de Devoluciones de la compañia EcoMarket |
| `Taller 2/Documentos/Terminos_y_Condiciones_Generales_de_Venta_EcoMarket.pdf` | PDF | Documento ejemplo de Términos y Condiciones Generales de Venta de la compañia EcoMarket |
| `Taller 2/Documentos/faq_ecomarket.json` | JSON | Documento ejemplo de Preguntas Frecuentes recopiladas para la compañia EcoMarket |
| `Taller 2/Documentos/inventario_productos_ecomarket.csv` | CSV | Documento ejemplo de Inventario de Productos de la compañia EcoMarket |
| `Taller 2/Documentos/pedidos_ecomarket.csv` | CSV | Documento ejemplo de Estados de Pedidos de la compañia EcoMarket |
| `Taller 2/Documentos/IAG_Taller_2_Fase3.ipynb` | Notebook (Colab / Jupyter) | Google Colab Notebook desarrollado para la Fase 3 de este Taller |
| `Taller 2/Documentos/README.md` | Markdown | Este archivo explicativo, con las fases I, II y III del Taller Nro. 2 |



# 🧠 Fase I: Selección de Componentes Clave del Sistema RAG para EcoMarket

---

## 🏗️ Contexto del Proyecto

**EcoMarket**, una empresa dedicada a la venta de productos sostenibles y en pleno proceso de crecimiento, ha enfrentado recientemente cuellos de botella en su servicio de atención al cliente. En algunos casos, los tiempos de respuesta han llegado hasta las 24 horas, lo que ha incrementado el índice de insatisfacción de los usuarios.

Nosotros, como especialistas en Inteligencia Artificial Generativa, hemos iniciado una asistencia técnica para abordar este problema. En la primera fase realizada, propusimos el uso de Modelos de Lenguaje Extenso (LLM), Modelos de Embeddings y Bases de Datos Vectoriales, con el objetivo de reducir los tiempos de respuesta y, al mismo tiempo, mejorar la satisfacción del cliente.

Los Large Language Models (LLM), si bien son potentes y de propósito general, no cuentan con conocimiento específico sobre la información interna de una empresa. Por esta razón, como equipo asesor, planteamos la implementación de un sistema de Generación Aumentada por Recuperación (RAG, Retrieval-Augmented Generation). Este enfoque permitirá que el LLM responda preguntas precisas basándose en documentos reales de la organización —como descripciones de productos, políticas internas o lineamientos de sostenibilidad—, reduciendo errores y evitando respuestas no fundamentadas (alucinaciones).

En esta etapa, como parte del equipo que asiste a EcoMarket, debemos seleccionar los dos componentes fundamentales del sistema RAG:

1. **El modelo de embeddings**, cuya elección dependerá de su precisión, costo y capacidad para manejar el idioma español.

2. **La base de datos vectorial**, que debe ofrecer eficiencia en las búsquedas, buena escalabilidad y facilidad de integración con el sistema.
---

## 🎯 Objetivo de la Fase I

Antes de iniciar la implementación, es necesario definir los dos componentes principales del sistema RAG:

1. **Modelo de Embeddings:** encargado de transformar el texto en vectores numéricos que representen su significado semántico.  
2. **Base de Datos Vectorial:** responsable de almacenar y recuperar esos vectores de manera eficiente, facilitando la búsqueda por similitud.

---

## 🧩 1. Decisión del Modelo de Embeddings

El **modelo de embeddings** convierte los textos de EcoMarket en **representaciones vectoriales** que capturan su significado.  
Para la empresa, es fundamental lograr **alta precisión semántica en español**, mantener **bajo costo operativo**, y asegurar la **posibilidad de escalamiento futuro**.

---

### 1.1. Opciones Evaluadas y Justificación

| **Modelo de Embedding** | **Tipo** | **Precisión en Español (RAG)** | **Costo por Uso** | **Limitaciones** | **Justificación de la Elección** |
|--------------------------|----------|---------------------------------|-------------------|------------------|----------------------------------|
| **BGE-M3 (BAAI General Embedding)** | Código Abierto (Hugging Face) | Alta. Excelente rendimiento multilingüe, optimizado para español. Soporta contexto largo (8192 tokens). | Costo cero (requiere infraestructura propia). | Necesita más recursos de cómputo (GPU/CPU). | Ofrece el mejor equilibrio entre precisión semántica, soporte multilingüe y control sobre los datos. Ideal para una empresa en desarrollo que busca evitar costos por API y mantener soberanía tecnológica. |
| **Multilingual E5-base** | Código Abierto (Hugging Face) | Buena. Ligero y eficiente, con resultados sólidos en español. | Costo cero. Muy eficiente en CPU. | Rendimiento algo inferior en recuperación semántica compleja. | Alternativa viable si se prioriza velocidad o disponibilidad de recursos limitados. |
| **OpenAI text-embedding-3-small** | Propietario (API de pago) | Muy alta. Resultados excelentes en español y gran consistencia vectorial. | Pago por cada texto procesado. | Dependencia de un proveedor externo. Costos acumulativos en grandes volúmenes. | Apropiado para entornos empresariales maduros con presupuesto para servicios en la nube. No recomendado en esta etapa inicial. |

---

### 1.2. 🏆 Modelo Seleccionado: **BGE-M3 (BAAI General Embedding)**

La propuesta de nuestro equipo es utilizar el modelo **BGE-M3**, de código abierto, desarrollado por **BAAI**.  

#### **Justificación técnica:**
- **Alto rendimiento** en tareas de búsqueda semántica en español.  
- **Soporte multilingüe**, ideal si EcoMarket expande operaciones a otros mercados.  
- **Costo nulo de licencia**, al ejecutarse localmente o en entornos cloud controlados por la empresa.  
- **Evita dependencia** de servicios externos, favoreciendo la privacidad de los datos internos.  

Esta elección permite a EcoMarket iniciar con un modelo potente y gratuito, con capacidad de escalar posteriormente a soluciones propietarias si se requiere mayor rendimiento o soporte.

---

## 🗃️ 2. Decisión de la Base de Datos Vectorial

La **Base de Datos Vectorial** es el componente que almacenará los embeddings generados y permitirá realizar búsquedas por similitud semántica.  
Para EcoMarket, los criterios clave son la **escalabilidad**, el **costo operativo** y la **facilidad de integración** con herramientas de desarrollo modernas (como LangChain o LlamaIndex).

---

### 2.1. Opciones Evaluadas y Justificación

| **Base de Datos** | **Tipo** | **Escalabilidad** | **Facilidad de Uso** | **Ventajas para EcoMarket** | **Desventajas** |
|-------------------|----------|-------------------|----------------------|-----------------------------|-----------------|
| **ChromaDB** | Vectorial pura / Open Source | Media (ideal para entornos de desarrollo o medianos volúmenes de datos). | Muy alta. Instalación simple y gran integración con frameworks de IA. | Costo cero. Rápida implementación local o cloud. Perfecta para validación de concepto o entornos en crecimiento. | No está diseñada para cargas de producción masivas. |
| **Qdrant** | Vectorial pura / Open Source | Alta. Optimizada para grandes volúmenes y rendimiento en producción. | Media. Requiere despliegue en contenedor (Docker o Kubernetes). | Permite búsquedas vectoriales y filtrado avanzado por metadatos (ej. “productos sostenibles”). | Configuración inicial más compleja. |
| **pgvector (PostgreSQL Extension)** | Extensión de base de datos SQL / Open Source | Media-Alta. Escalable dentro del ecosistema PostgreSQL. | Alta. Ideal si la empresa ya usa PostgreSQL. | Permite integrar datos vectoriales y estructurados en un mismo entorno. Cumple con ACID. | No es una base vectorial pura; menor rendimiento frente a Qdrant o Pinecone en escalas grandes. |
| **Pinecone** | Propietario (SaaS) | Muy alta. Totalmente administrada en la nube. | Alta. Integración sencilla por API. | Escalabilidad inmediata y soporte empresarial. | Costos por volumen de datos y dependencia total de un proveedor externo. |

---

### 2.2. 🏆 Base de Datos Seleccionada: **ChromaDB**

Proponemos **ChromaDB** como base de datos vectorial inicial para EcoMarket.

#### **Justificación técnica y estratégica:**
- **Simplicidad de implementación:** se integra fácilmente con pipelines de RAG usando Python y librerías como LangChain.  
- **Costo cero:** al ser open source, no implica gastos de licencia o suscripción.  
- **Ideal para un entorno en desarrollo:** permite concentrar esfuerzos en la optimización del flujo de embeddings y recuperación antes de escalar.  
- **Compatibilidad con diferentes modelos:** se adapta fácilmente a cambios futuros de modelo de embeddings o infraestructura.
  
---
## 🧠 3. Arquitectura RAG Propuesta

El sistema RAG propuesto para EcoMarket seguirá la siguiente arquitectura base:

```text
Documentos de EcoMarket
        │
        ▼
   BGE-M3 (Embeddings)
        │
        ▼
Vectores Numéricos
        │
        ▼
   ChromaDB (Almacenamiento y Búsqueda)
        │
        ▼
   LLM (Generación de Respuestas)

```
---

# 🧠 Fase II: Construcción de la Base de Conocimiento (Indexación y Segmentación)

En esta fase se construye la base de conocimiento del sistema RAG (Retrieval-Augmented Generation). El proceso consiste en segmentar los documentos procesados y almacenarlos en una base de datos vectorial utilizando un modelo de embeddings especializado. Esta etapa es fundamental para que el sistema pueda recuperar información relevante de manera semántica ante una consulta del usuario.

## 1. Segmentación de los documentos

Previo a la indexación, los textos son divididos en fragmentos manejables con el objetivo de optimizar la recuperación semántica. La segmentación se realiza empleando un Text Splitter, el cual corta los documentos en bloques con una longitud máxima controlada (por ejemplo, 1.000 caracteres) y un solapamiento entre ellos (por ejemplo, 200 caracteres). Este solapamiento permite preservar el contexto entre fragmentos contiguos y evita pérdida de información en los límites de los textos.

Cada fragmento resultante mantiene una relación directa con el documento original, asegurando trazabilidad y precisión durante el proceso de recuperación posterior. El resultado de esta etapa son los documentos segmentados (final_docs), que sirven como insumo para la generación de embeddings.

## 2. Generación de embeddings con BGE-M3

Una vez segmentados los textos, se generan sus representaciones vectoriales mediante el modelo BGE-M3, alojado en Hugging Face. Este modelo convierte los fragmentos de texto en vectores de alta dimensión que capturan el significado semántico de cada fragmento.

El modelo se inicializa de la siguiente forma:

model_name: "BAAI/bge-m3"

model_kwargs: define que la ejecución se realice en GPU ('device': 'cuda') para aprovechar la aceleración de cómputo.

encode_kwargs: incluye la normalización de los embeddings ('normalize_embeddings': True), lo que mejora la coherencia en las comparaciones vectoriales.

Este proceso garantiza que los embeddings mantengan relaciones espaciales consistentes, permitiendo medir la similitud entre consultas y documentos.

## 3. Indexación en la base de datos vectorial (ChromaDB)

Con los embeddings generados, se construye la base de datos vectorial utilizando ChromaDB. Esta herramienta almacena los vectores en un formato optimizado para búsquedas de similitud, lo cual permite recuperar los documentos más relevantes en función del significado de la consulta, no solo de coincidencias léxicas.

Durante la creación de la base vectorial:

Se asigna un nombre a la colección (collection_name="ecomarket_rag_data") que identifica el conjunto de embeddings.

Se define un directorio local para persistir los datos (persist_directory="./chroma_db"), lo que permite reutilizar la base sin recalcular los embeddings en ejecuciones futuras.

A partir de la base Chroma creada, se construye un retriever, encargado de buscar los fragmentos más cercanos semánticamente a la consulta del usuario. En este caso, se define que recupere los tres documentos más relevantes (k=3) mediante una búsqueda basada en similitud de coseno.

## 4. Resultado final

Al finalizar la fase, la base vectorial queda configurada y lista para integrarse en el flujo del modelo RAG. Esta estructura permite que, ante una pregunta, el sistema recupere los fragmentos más semánticamente relacionados y los use como contexto para generar una respuesta precisa y fundamentada.

# 🧠 Fase III: Integración y Ejecución del Código

Para esta fase hemos desarrollado el **Google Colab Notebook** con el nombre `IAG_Taller_2_Fase3.ipynb`, donde implementamos el **modelo LLM Mistral-7B Instruct** ([Hugging Face](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)), el mismo utilizado en el **Taller Práctico N.º 1**.  
En este notebook construimos además un **modelo RAG (Retrieval-Augmented Generation)** empleando como **modelo de embeddings** `BAAI/bge-m3` y como **base de datos vectorial** `ChromaDB` y usando documentos que hemos creado que nos permiten que las busquedas se hagan en información propia de la compañia, permitiendo asi que sea el contexto usado por el Modelo LLM al responder a las preguntas que se simulan con usuarios o clientes.  

El archivo puede ejecutarse directamente en **Google Colab**, configurando el entorno de ejecución con **T4 GPU** y **High RAM**.  
Al ejecutar las celdas en orden, se podrá observar:  
- La carga de librerías y módulos requeridos.  
- La construcción del modelo RAG con `BAAI/bge-m3` y `ChromaDB` con seis (6) documentos: Inventario de Productos (Formato CSV), Estados de Pedidos (Formato CSV), Políticas de Devolución de EcoMarket (Formato PDF), Terminos Generales de Ventas de EcoMarket (Formato PDF), Manuales de Usuario de Productos (Formato PDF), y Preguntas Frecuentes (Formato JSON).
- La carga del modelo LLM **Mistral-7B** en modo 4-bit.  
- La generación de *prompts* y respuestas basadas en el modelo RAG, presentadas en el **Paso N.º 11**, donde se muestran los resultados obtenidos frente a las preguntas de prueba.
