# 🧠 Fase 1: Selección de Componentes Clave del Sistema RAG — EcoMarket

---

## 🏗️ Contexto del Proyecto

**EcoMarket** es una empresa en desarrollo que busca optimizar la gestión y acceso a su información interna mediante un sistema de **Generación Aumentada por Recuperación (RAG, Retrieval-Augmented Generation)**.  

Este sistema permitirá a un **Large Language Model (LLM)** responder preguntas precisas basándose en documentos reales de la empresa —como descripciones de productos, políticas internas o lineamientos de sostenibilidad—, reduciendo errores y evitando respuestas no fundamentadas (*alucinaciones*).  

Como grupo de **estudiantes de la asignatura de Inteligencia Artificial Generativa**, proponemos la arquitectura inicial de este sistema RAG. En esta primera fase se abordan las decisiones críticas de **arquitectura** que determinarán su rendimiento, escalabilidad y costo.

---

## 🎯 Objetivo de la Fase 1

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

### 2.3. 🚀 Ruta de Escalabilidad Futura

En fases posteriores, EcoMarket podría considerar:
- **Migrar a Qdrant**, si requiere búsquedas vectoriales a gran escala con filtrado avanzado de productos o categorías.  
- **Adoptar pgvector**, si se desea integrar información vectorial directamente en su base de datos relacional principal (PostgreSQL).  
- **Usar Pinecone Cloud**, en caso de crecimiento masivo y necesidad de un servicio administrado de alta disponibilidad.

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
