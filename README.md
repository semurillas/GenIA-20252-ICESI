# GenIA-20252-ICESI
This repository will host all projects in the field of generative artificial intelligence.


```mermaid
graph TD
    subgraph "Entrada de Consulta"
        A[Cliente (Chat, Email, RRSS)] --> B{Módulo de Clasificación};
    end

    subgraph "Flujo Automatizado (Respuestas Repetitivas)"
        subgraph "Modelo de Clasificación (BART)"
            B --> C{Tipo de Consulta?};
            C -- "80% Consultas Repetitivas" --> D[Consulta es sobre Pedido, Devolución, Producto];
        end

        subgraph "Modelo de Respuestas Automáticas (T5)"
            D --> E[T5 se conecta a la Base de Datos de EcoMarket];
            E --> F[Genera Respuesta Personalizada];
            F --> G[Respuesta Rápida Enviada al Cliente];
        end
    end

    subgraph "Flujo Humano Asistido (Consultas Complejas)"
        subgraph "Modelo de Clasificación (BART)"
            C -- "20% Consultas Complejas" --> H[Consulta es sobre Queja, Problema Técnico];
        end

        subgraph "Asistente de IA (GPT-3.5)"
            H --> I[GPT-3.5 asiste al Agente de Soporte];
            I --> J[Genera Borradores de Respuesta y Resúmenes];
            J --> K[Agente Humano Edita y Personaliza];
            K --> L[Respuesta con Empatía Enviada al Cliente];
        end
    end

    style B fill:#f9f,stroke:#333,stroke-width:2px;
    style C fill:#9cf,stroke:#333,stroke-width:2px;
    style D fill:#cff,stroke:#333,stroke-width:2px;
    style E fill:#cff,stroke:#333,stroke-width:2px;
    style F fill:#cff,stroke:#333,stroke-width:2px;
    style G fill:#f9f,stroke:#333,stroke-width:2px;
    style H fill:#fcc,stroke:#333,stroke-width:2px;
    style I fill:#fcc,stroke:#333,stroke-width:2px;
    style J fill:#fcc,stroke:#333,stroke-width:2px;
    style K fill:#fcc,stroke:#333,stroke-width:2px;
    style L fill:#f9f,stroke:#333,stroke-width:2px;

    classDef proceso fill:#e0f7fa,stroke:#333;
    class A,G,L proceso;
```mermaid
