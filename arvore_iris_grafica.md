# Visualização da Árvore de Decisão

```mermaid
graph TD
    Node0["petallength <= 2.45"]
    style Node0 fill:#a7d8f0,stroke:#333,stroke-width:2px
    Node0 -- "Sim" --> Node0_0
    Node0_0(["Iris-setosa"])
    style Node0_0 fill:#a7f0a7,stroke:#333,stroke-width:2px
    Node0 -- "Não" --> Node0_1
    Node0_1["petalwidth <= 1.75"]
    style Node0_1 fill:#a7d8f0,stroke:#333,stroke-width:2px
    Node0_1 -- "Sim" --> Node0_1_0
    Node0_1_0["petallength <= 4.95"]
    style Node0_1_0 fill:#a7d8f0,stroke:#333,stroke-width:2px
    Node0_1_0 -- "Sim" --> Node0_1_0_0
    Node0_1_0_0["sepallength <= 4.95"]
    style Node0_1_0_0 fill:#a7d8f0,stroke:#333,stroke-width:2px
    Node0_1_0_0 -- "Sim" --> Node0_1_0_0_0
    Node0_1_0_0_0(["Iris-virginica"])
    style Node0_1_0_0_0 fill:#a7f0a7,stroke:#333,stroke-width:2px
    Node0_1_0_0 -- "Não" --> Node0_1_0_0_1
    Node0_1_0_0_1(["Iris-versicolor"])
    style Node0_1_0_0_1 fill:#a7f0a7,stroke:#333,stroke-width:2px
    Node0_1_0 -- "Não" --> Node0_1_0_1
    Node0_1_0_1["petalwidth <= 1.55"]
    style Node0_1_0_1 fill:#a7d8f0,stroke:#333,stroke-width:2px
    Node0_1_0_1 -- "Sim" --> Node0_1_0_1_0
    Node0_1_0_1_0(["Iris-virginica"])
    style Node0_1_0_1_0 fill:#a7f0a7,stroke:#333,stroke-width:2px
    Node0_1_0_1 -- "Não" --> Node0_1_0_1_1
    Node0_1_0_1_1(["Iris-versicolor"])
    style Node0_1_0_1_1 fill:#a7f0a7,stroke:#333,stroke-width:2px
    Node0_1 -- "Não" --> Node0_1_1
    Node0_1_1(["Iris-virginica"])
    style Node0_1_1 fill:#a7f0a7,stroke:#333,stroke-width:2px
```