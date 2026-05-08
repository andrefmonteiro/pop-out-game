# Handover — Estado do Projeto

## O que já está feito

### 1. MCTS — Torneios e escolha do melhor modelo

Corremos dois torneios para comparar versões do algoritmo MCTS (Monte Carlo Tree Search):

- **Torneio 1**: 4 variantes com diferentes números de iterações, constante de exploração (c) e largura de expansão. O vencedor foi o **DeepThinker** (200 iterações).
- **Torneio 2**: 4 sub-variantes do DeepThinker, variando `c` e `expansion_count`. O vencedor foi o **DT-Wide** (iterações=200, c=1.414, expansion_count=2).

Os gráficos dos resultados (heatmaps e bar charts) já foram gerados e estão em:
- `src/mcts_tournament/graphs/` — Torneio 1
- `src/mcts_tournament/graphs/` — Torneio 2 (prefixo `2nd_tournament_`)

### 2. Dataset do PopOut

Corremos o modelo DT-Wide contra si próprio para gerar pares *(estado do tabuleiro, movimento)*.

- Ficheiro: `popout_dataset.csv` (raiz do repositório)
- **15 553 linhas / 1 185 jogos**
- Cada linha: `game_id`, 42 células do tabuleiro (`r0c0` a `r5c6`, valores 0/1/2), `move` (ex: `DROP_3`, `POP_1`)
- Para gerar mais dados (não é necessário): `venv/bin/python main_datasets.py`

### 3. Algoritmo ID3 — implementado e testado

O ID3 está implementado de raiz (sem scikit-learn) em `src/decision_tree/decision_tree_id3.py`.

Funções disponíveis:
- `build_tree(data, features, label_col, numerical_features, max_depth)` — treina a árvore
- `predict(node, example)` — classifica um exemplo
- `print_tree(node, max_print_depth)` — imprime a árvore em texto
- `evaluate(node, test_data, label_col)` — retorna a accuracy no conjunto de teste
- `tree_stats(node)` — retorna profundidade, nº de nós, folhas, nós internos
- `train_test_split(data, test_ratio, seed)` — divide os dados em treino/teste
- `load_csv(filepath)` — lê um CSV para lista de dicts
- `save_results(results, filepath)` — guarda resultados num CSV

**Iris (warm-up)** — já testado:
```
venv/bin/python src/decision_tree/decision_tree_id3.py
```
Resultado: árvore com profundidade 4, 11 nós, accuracy de treino 100%, accuracy de teste 90%.
Este resultado vai direto para o notebook — não precisa de CSV separado.

---

## O que falta fazer

### Passo 1 — Depth sweep no dataset PopOut

Correr o ID3 com vários valores de `max_depth` para encontrar o equilíbrio entre underfitting e overfitting.

**Como correr**: copiar o bloco `# POPOUT` do final de `src/decision_tree/decision_tree_id3.py` para uma célula do notebook (ou um script) e correr a partir da raiz do repositório.

Valores a testar: `[1, 3, 5, 7, 10, 15, 20, 30, None]`

**Os resultados são guardados automaticamente** em `id3_popout_results.csv` (raiz do repo). Este ficheiro é a fonte de verdade para os gráficos — pode ser regenerado a qualquer altura sem voltar a correr o modelo.

Depois de correr, preencher a tabela de resultados em `notebook_notes.md`.

### Passo 2 — Gráfico accuracy vs profundidade

```bash
venv/bin/python src/decision_tree/visualize_id3.py
```

Lê `id3_popout_results.csv` → guarda `src/decision_tree/graphs/popout_accuracy_vs_depth.png`.
Pode ser re-corrido a qualquer altura para mudar cores, estilo, etc.

### Passo 3 — Notebook Jupyter

Estrutura (ver `notebook_notes.md` para talking points completos):

1. **Secção MCTS** — explicar o algoritmo UCT, mostrar resultados dos torneios (inserir os PNGs já gerados), justificar a escolha do DT-Wide
2. **Secção Iris** — correr o `__main__` do `decision_tree_id3.py` inline, mostrar árvore + accuracy, explicar discretização
3. **Secção PopOut** — tabela de resultados do depth sweep + gráfico, discutir tradeoffs ID3 vs MCTS

### Passo 4 — Slides de apresentação (PDF, máx. 10 minutos)

Talking points já estão em `notebook_notes.md` na secção "Presentation talking points".

---

## Ficheiros importantes

| Ficheiro | O que é |
|---|---|
| `todo.md` | Checklist com comandos para cada passo |
| `notebook_notes.md` | Decisões, métricas, tradeoffs e talking points para o notebook |
| `src/decision_tree/decision_tree_id3.py` | ID3 implementado — ler o bloco TODO no final |
| `src/decision_tree/visualize_id3.py` | Gera o gráfico a partir do CSV de resultados |
| `id3_popout_results.csv` | Resultados do depth sweep (criado no Passo 1) |
| `popout_dataset.csv` | Dataset gerado pelo MCTS (15k+ linhas) |
| `first_tournament_results.csv` | Resultados Torneio 1 |
| `second_tournament_results.csv` | Resultados Torneio 2 |
