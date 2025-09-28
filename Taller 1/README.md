<h1> <img width="207" height="112" alt="image" src="https://github.com/user-attachments/assets/89fd906b-04fb-4d4f-b5e6-8375083a8a01" /></h1>
<h1>📚 Maestría en Inteligencia Artificial Aplicada – 3er Semestre</h1>

<h3>Asignatura: Inteligencia Artificial Generativa</h3>

<h3>Taller Práctico Nro. 1 </h3>

<hr style="width:60%;">

<h3>👨‍🎓 Estudiantes</h3>
<ul style="list-style:none; padding:0; font-size:18px;">
    <li>Sebastián Murillas</li>
    <li>Octavio Guerra</li>
</ul>

<hr style="width:60%;">

<h3>📅 Fecha: Septiembre 26, 2025</h3>

---
# Fase I - Propuesta de Arquitectura IAG para Optimización del servicio al Cliente de la compañia EcoMarket


Tras revisar la literatura y la documentación sobre Modelos de Lenguaje Grande (LLM) y la teoría de la Inteligencia Artificial Generativa, nosotros proponemos una solución **Híbrida**. Este enfoque busca mitigar el impacto negativo de los altos tiempos de respuesta (24 horas en promedio) en la métrica de **Satisfacción del Cliente** de la compañia **EcoMarket**, en conjunto con un manejo costo-eficiencia, que es importante para la compañia.

---

## 1. Arquitectura General

Nuestro Modelo Híbrido está compuesto por:

1. **Modelo Fine Tuned LLM**, para atender el **80%** de las consultas repetitivas. Ejemplos: GPT-4omini, Gemini 1.5 Flash, Mistral 7B Instruct 
2. **Modelo LLM** de propósito general, para atender las consultas o preguntas complejas (**20%**). Ejemplos: GPT-4, Claude 3.5 Sonnet.

### ¿Por qué?

Esta arquitectura permite que el modelo Fine-Tuned se enfoque en **eficiencia**, mientras que el LLM aporta **capacidad de comprensión** en consultas complejas.  
Esto resolverá el problema más importante de EcoMarket: **reducir los tiempos de respuesta que hoy son de  24 horas  a minutos** con el uso de LLM .  

En cuanto a costos, usar un esquema Híbrido permite:  
- Operar con un **presupuesto moderado** para resolver la parte repetitiva.  
- **Estimar un costo límite máximo** al usar un LLM en los casos complejos.  

La elección del modelo se basa en un análisis de **costo-beneficio** centrado en la tarea específica que debe resolver cada componente.

---

### 1.1. Para el 80% de Consultas (Repetitivas: Pedidos, Devoluciones, Catálogo)

**Modelo Elegido (Ejemplo):** LLM Ligero y Open Source (e.g., *Mistral 7B*) + Afinamiento (Fine-Tuning)

| Criterio               | Justificación |
|-------------------------|---------------|
| **Necesidad de Precisión** | Alta. Una respuesta incorrecta sobre el estado de un pedido (ej: "entregado" cuando está "en camino") es crítica para la satisfacción. |
| **Ventaja del Afinamiento** | Al aplicar Fine-Tuning sobre un modelo ligero base (como Mistral 7B), el modelo aprende el vocabulario, la estructura de las preguntas frecuentes y el tono de EcoMarket. Esto permite rapidez y precisión en su dominio. |
| **Costo Operacional** | Bajo. Los modelos ligeros son más baratos de alojar en infraestructura propia o en la nube. Solo se activan cuando se requieren, manejando eficientemente el alto tamaño de preguntas que recibirá. |

---

### 1.2. Para el 20% de Consultas (Complejas: Quejas, Problemas, Sugerencias)

**Modelo Elegido (Ejemplo):** LLM de Propósito General de Alto Rendimiento (e.g., *GPT-4o, Gemini 1.5 Pro*)

| Criterio               | Justificación |
|-------------------------|---------------|
| **Necesidad de Fluidez/Razonamiento** | Alta. Estas consultas exigen comprender el contexto emocional (empatía), sintetizar información de múltiples fuentes y seguir instrucciones complejas. |
| **Ventaja de Rendimiento** | Modelos como GPT-4o y Gemini 1.5 Pro poseen razonamiento en cadena (*chain-of-thought*) y uso de herramientas (*Function Calling*). Esto es esencial para clasificar correctamente la queja y determinar a qué agente o departamento derivarla, proporcionando al humano un resumen pre-analizado. |
| **Costo Operacional** | Moderado/Alto. El costo por token es mayor, pero al representar solo el 20% del volumen de tráfico, la inversión se justifica porque impacta directamente en la **Satisfacción del Cliente**. |

---

## 2. Arquitectura Propuesta

Nuestra arquitectura es un **sistema de Orquestación** con **decisión basada en el tráfico**, combinando modelos Fine-Tuned con LLM de Propósito General.

```mermaid
graph TD
    subgraph "Entrada de Consulta"
        A["Cliente: Chat, Email, RRSS"] --> B["Orquestador / Router"];
    end

    subgraph "Clasificación - Router Ligero"
        B -- "80% Consultas Repetitivas" --> C["Pedidos, Devoluciones, Catálogo"];
        B -- "20% Consultas Complejas" --> G["Quejas, Problemas, Sugerencias"];
    end

    subgraph "Ruta 80% - Consultas Repetitivas"
        C --> D["LLM Fine-Tuned - Ej: Mistral 7B, LLaMA 2-7B"];
        D --> E["RAG conectado a BD de EcoMarket"];
        E --> F["Genera Respuesta Personalizada"];
        F --> Z["Respuesta Automática Enviada al Cliente"];
    end

    subgraph "Ruta 20% - Consultas Complejas"
        G --> H["LLM Potente - Ej: GPT-4o, Gemini 1.5 Pro, Claude 3 Opus"];
        H --> I["Function Calling / Integración CRM & Tickets"];
        I --> J["Genera Resumen o Acción"];
        J --> K["Agente Humano Ajusta y Envía"];
    end

    %% Estilos
    style A fill:#D4E6F1,stroke:#333,stroke-width:2px;
    style B fill:#AED6F1,stroke:#333,stroke-width:2px;

    style C fill:#C0F6C0,stroke:#333,stroke-width:2px;
    style D fill:#C0F6C0,stroke:#333,stroke-width:2px;
    style E fill:#C0F6C0,stroke:#333,stroke-width:2px;
    style F fill:#C0F6C0,stroke:#333,stroke-width:2px;
    style Z fill:#D4E6F1,stroke:#333,stroke-width:2px;

    style G fill:#F6C0C0,stroke:#333,stroke-width:2px;
    style H fill:#F6C0C0,stroke:#333,stroke-width:2px;
    style I fill:#F6C0C0,stroke:#333,stroke-width:2px;
    style J fill:#F6C0C0,stroke:#333,stroke-width:2px;
    style K fill:#F6C0C0,stroke:#333,stroke-width:2px;
```
### 2.1. Arquitectura Lógica

1. **Orquestador/Enrutador:**  
   - Recibe cada consulta del cliente.  
   - Usa un modelo ligero (ej: *GPT-4o Mini*) afinado para clasificación.  
   - Decide: ¿Es repetitiva (80%) o compleja (20%)?  

2. **Ruta del 80% (Eficiencia):**  
   - La consulta pasa al **Modelo Fine-Tuned LLM**.
   - Este modelo integra una capa de **Generación Aumentada por Recuperación (RAG)** para interactuar con la Base de Datos de EcoMarket (solo lectura de datos estáticos y fácticos, ej. estados de envío, descripción de productos, devoluciones).

3. **Ruta del 20% (Capacidad):**
   - Si es compleja, la consulta pasa al **Modelo LLM**.
   - Este modelo usa la funcionalidad de Llamada a Funciones **(Function Calling)** para iniciar procesos especializados (ej: registrar una queja en el CRM o generar un ticket de soporte).
   - Si el modelo determina que la pregunta supera su capacidad de resolución (ej. requiere una negociación con el cliente), lo envía a un Agente de Call Center, acompañado de un **resumen** y un **sentiment score**.
   
---

### 2.2. Integración con la Base de Datos (BD) de EcoMarket

| Mecanismo de Integración | Propósito | Aplicación en EcoMarket |
|--------------------------|-----------|--------------------------|
| **RAG (Retrieve Augmented Generation)** | Consultar datos en tiempo real (solo lectura). | Estado del pedido, información de envío, inventario y catálogo. |
| **Function Calling / Herramientas** | Ejecutar acciones o registrar datos (lectura y escritura). | Registrar una devolución, actualizar el status de una queja, o ejecutar un script de diagnóstico para un problema técnico, ej.: Pedido no registrado, falla en acceso al portal de Ecomarket, etc. |

---

## 3. Justificación

| Criterio               | Justificación |
|-------------------------|---------------|
| **Costo** | Optimización del TCO. El 80% del tráfico va a un LLM Fine-Tuned económico (ej. Mistral 7B). Solo se paga un modelo premium para el 20% de casos críticos. |
| **Escalabilidad** | Escalabilidad paralela: el 80% se maneja con clusters de modelos ligeros en GPUs económicas. El 20% escala en la nube de proveedores de LLM de alto nivel (OpenAI/Google). |
| **Facilidad de Integración** | Uso de estándares como RAG y Function Calling, lo que simplifica el desarrollo y reduce la curva de aprendizaje del equipo de ingeniería. |
| **Calidad de Respuesta** | Precisión garantizada en el 80% repetitivo (Fine-Tuning + RAG) y razonamiento superior en el 20% complejo (uso modelos avanzado). |

---

# Fase II - Evaluación de Fortalezas, Limitaciones y Riesgos Éticos

### 4. Fortalezas
- **Reducción en los Tiempos de Respuesta de Servicio al Cliente:**  
  Es definitivamente el principal beneficio. El 80% de las consultas se resuelven en minutos, no en horas, impactando de manera benéfica la métrica **Satisfacción del Cliente**.

- **Disponibilidad 24/7:**  
  Por ser un modelo "Fine Tuned LLM", estará disponible de manera continua, 7x24, para manejar el alto volumen de consultas repetitivas. Esto de nuevo, redunda de manera positiva en la **Satisfacción al Cliente**.

- **Coherencia y Consistencia:**  
  Se asegura una única fuente de información para el 80% de las preguntas, eliminando las variaciones y errores que surgen de la respuesta humana. En otras palabras, reducción en las respuestas erróneas, inconsistentes o demoras en las respuestas.

- **Especialización de la Labor del Agente Humano:**  
  Los agentes se liberan del trabajo repetitivo, pudiendo enfocarse solo en el 20% de los casos complejos, donde su empatía y pensamiento crítico son realmente valiosos.

---

### 5. Limitaciones
- **Limitación en la Empatía:**  
  Si bien se ofrece un "fine tuned LLM" al igual que un Modelo LLM para responder a lo repetitivo y lo complejo. En los casos donde se requiere negociación o manejo de crisis, estos modelos no pueden replicar la inteligencia emocional de un agente humano. Es por eso, que el Agente de Call Center debe atender al cliente en estas situaciones.

- **Dependencia en la Calidad de los Datos:**  
  Si queremos contar con una precisión mayor o igual al 80%, dependeremos completamente de la exactitud y limpieza de la **Base de Datos de EcoMarket**.  
  Si hay errores, información incompleta, muy pocos datos o inventados, el **LLM Fine-Tuned** generará respuestas erroneas o equivocadas. Esto afectara la **Satisfacción al Cliente** y pondrá en riesgo la reputación de la compañia. Es lo siempre se maneja como lema con la Inteligencia Artificial: **Basura (Garbage)** genera **Basura (Garbage)**

- **Costos de Entrenamiento (Fine-Tuning):**  
  La inversión inicial en tiempo y recursos para afinar y hostear el modelo y genere una precisión mayor o igual al 80% puede ser significativa.Pero creemos que será menor a usar un modelo LLM que tiene costos de Tokens y llamadas API. Aquí sera importante, planear adecuadamente para que los costos no sean altos y echen por tierra este proyecto.

---

### 6. Riesgos Éticos y de Gobernanza de Datos
- **Alucinaciones:**  
  Siempre existe el riesgo de que LM  invente información (una *"alucinación"*) al generar datos de pedidos, productos, un resumen o un diagnóstico complejo.  
  *Mitigación:* Implementar filtros de verificación de hechos en la fase de **Function Calling** antes de generar la respuesta al cliente y mecanismo de validación de respuestas a las preguntas repetitivas.

- **Sesgo:**  
  Si los datos utilizados para el Fine-Tuning contienen sesgos históricos (ej. si las quejas de un grupo demográfico específico fueron mal manejadas históricamente), el modelo podría perpetuar y automatizar ese trato preferencial o injusto.  
  *Mitigación:* Auditoría de sesgos en el dataset de entrenamiento y en las respuestas generadas.

- **Privacidad de Datos:**  
  Al integrar la BD de clientes (direcciones, historial de compras, entre otros) en el contexto de los prompts (ya sea **RAG** o **Function Calling**), se debe asegurar que:  
  1. Los datos están anonimizados o se accede solo a la información mínima necesaria.  
  2. Se implementa un estricto control de acceso y almacenamiento temporal del contexto (*borrado inmediato después de la respuesta*).
  3. Autenticación de usuarios para identificar quién accede y tener una auditoría de todo el flujo de interacción.
  4. Usar un "Servicio Intermedio" para evitar que alguno de los modelos LLM usados interactué directamente con la o las bases de datos de **EcoMarket**

- **Impacto Laboral:**
  Los cambios Tecnologicos o de algun otro tipo en las compañias siempre generan incertidumbre en la fuerza laboral activa. Tenemos clara que habrá reducción del personal actual de Agentes usado para el servicio al cliente. Debemos manter como objetivo claro: que se trata de **mejorar, empoderar y no reemplazar**. La propuesta debe ser vista por EcoMarket como una herramienta que eleva el trabajo de los agentes de soporte, permitiéndoles enfocarse en la calidad y la retención del cliente, en lugar de en la cantidad de tickets repetitivos que son lo que a hoy esta desbordado, haciendolo ineficiente y alta tasa de insatisfacción de los clientes; crítico para una compañia emergente como EcoMarket.

  # Fase III - Aplicación de Ingeniería de Prompts

  A continuación presentamos los propmts que hemos diseñado para los dos (2) requerimientos que se solicitan.

  ### 1. Estado de Solicitud de Pedido

  prompt_pedido = f"""
Eres un agente de servicio al cliente amable, profesional y conciso.
Tu única tarea es proporcionar el estado del pedido {num_pedido} con un **lenguaje natural y conversacional**, basándote estrictamente en la siguiente información:

- **Número de Pedido:** {num_pedido}
- **Estado Actual:** {estado}
- **Fecha de Entrega Estimada:** {estimacion_formateada}
- **Retrasado:** {retrasado}
{instruccion_tracking_data}

**INSTRUCCIONES DE FORMATO DE RESPUESTA:**
1.  Comienza con una frase que indique el estado y la estimación de entrega (si aplica), usando el formato: "Su orden {num_pedido} se encuentra {frase_estado}. La fecha de entrega estimada es {estimacion_formateada}."
2.  Si la estimación es 'No aplica' (como en el caso de 'Cancelado' o 'Entregado'), omite la parte de la fecha de entrega, solo indica el estado.
{instruccion_tracking}4. Si **Retrasado** es True, añade el siguiente mensaje al final: "Nos excusamos por la demora en la entrega y estamos trabajando para que pueda contar con su orden lo mas pronto posible."
5.  Si el **Estado Actual** es 'Cancelado', añade el siguiente mensaje al final: "Lamentamos los inconvenientes y le invitamos a comunicarse con nuestro centro de servicios al Nro. 01-800-XXX-XXXX para tener más detalles."
6.  **IMPORTANTE:** Tu respuesta NO debe contener encabezados, listas numeradas, ni repetir la información de entrada, solo debe generar el texto conversacional.

Respuesta:
"""

  ### 2. Devolución de Producto

     prompt = f"""
Actúa como un agente de servicio al cliente amable y profesional.
Usa la siguiente base de datos de productos:

{base_datos_devoluciones}

Instrucciones para el Asistente:
1. Responde inmediatamente al cliente siguiendo las instrucciones de formato.
2. Identifica el producto por su ID (ej. Producto 2002) y su nombre.
3. Revisa si el producto es retornable.
4. Si es retornable, indica **Retornable** y explica el proceso.
5. Si NO es retornable, indica **No retornable**, explica la razón y ofrece alternativas/descuentos.
6. Da la respuesta en el siguiente formato:
    - **Estado del producto**: (Retornable / No retornable)
    - **Explicación**
    - **Siguientes pasos / Alternativas**
7. Mantén la respuesta clara y concisa, máximo 5 párrafos.
8. Usa un tono cálido, humano y profesional.

---
Cliente: Hola, estoy devolviendo {producto_buscado} por {motivo}, ¿qué debo hacer?

{MARCADOR_ASISTENTE}"""

### 3. Prueba de los PROMPTS

Nosotros creamos un Google Colab Notebook que se llama IAG_Taller1_Fase_3, donde hicimos pruebas de los dos (2) Prompts diseñados. Este Google Colab Notebook esta en este repositorio de GitHUb y puede ser probado dando "Clic" con el ratón en el icono "Open Google Colab".
