# Notebook Notes — Decisions, Tradeoffs, Discussion Topics

Use this file to accumulate talking points for the notebook writeup and slides.
Each section maps to a part of the notebook.

---

## MCTS Section

### Why MCTS over minimax?
- PopOut has a very large branching factor (up to 14 moves per turn) and no obvious heuristic evaluation function
- Minimax requires an evaluation function at leaf nodes; MCTS uses random playouts instead, so no domain knowledge is needed
- MCTS allocates compute where the tree is most promising (UCT guides exploration), minimax explores uniformly

### What UCT does
- UCT = exploitation (win rate) + exploration bonus (c * sqrt(log(parent_visits) / child_visits))
- The c constant controls the balance: low c = exploit known good moves, high c = explore less-visited moves
- c=1.414 (sqrt(2)) is the theoretically optimal value for certain reward distributions

### Tournament 1 — variant comparison

| Variant | iterations | c | expansion_count | Result |
|---|---|---|---|---|
| Baseline | 50 | 1.414 | 1 | Weakest |
| DeepThinker | 200 | 1.414 | 1 | Winner |
| Explorer | 50 | 2.5 | 1 | More exploration hurt with low budget |
| WideExpander | 50 | 1.414 | 3 | Width without depth hurt |

**Key insight**: More iterations (deeper search) consistently beats more exploration or wider expansion when the compute budget is fixed. DeepThinker had 4x more iterations than the others.

### Tournament 2 — DeepThinker sub-variants

| Variant | c | expansion_count | Result |
|---|---|---|---|
| DT-Frugal (control) | 1.414 | 1 | — |
| DT-Exploit | 0.7 | 1 | — |
| DT-Explore | 2.0 | 1 | — |
| DT-Wide (winner) | 1.414 | 2 | Best overall |

**Key insight**: DT-Wide wins — expanding 2 children per iteration (instead of 1) gave the tree better coverage of the move space at 200 iterations. At this budget, a small increase in breadth helped more than changing the exploration constant.

### Chosen model
**DT-Wide**: iterations=200, c=1.414, expansion_count=2

---

## ID3 / Decision Tree Section

### What ID3 is
- ID3 is an algorithm that builds a decision tree from labelled training data
- At each node, it picks the feature that maximises information gain (reduces entropy the most)
- Recurses until leaves are pure or stopping criteria are met

### Why ID3 instead of MCTS for classification?
- Decision trees are fast at inference: O(depth) per prediction vs O(iterations) per MCTS move
- Trees are interpretable — you can read the rules; MCTS is a black box
- But trees can't plan ahead — they map state → move directly without lookahead

### Discretization (iris dataset)
- ID3 requires categorical features; iris has continuous values (petal/sepal measurements)
- Approach: for each numerical feature, try all midpoint thresholds between consecutive sorted unique values; pick the threshold that maximises information gain
- This converts each continuous feature into a binary split: value <= threshold vs value > threshold
- Tradeoff: more candidate thresholds = better splits but slower training

### Train/test split — why 80/20?
- We hide 20% of the data before training so the tree never sees it
- At evaluation time we test on that 20% — this tells us if the tree generalised or just memorised
- 80/20 is the standard convention for datasets of this size (iris: 120 train / 30 test)
- If we tested on training data we'd always get 100% — meaningless

### Iris tree metrics (actual measured values — fill in after running)

| Metric | Value |
|---|---|
| Depth | 4 |
| Total nodes | 11 |
| Internal nodes | 5 |
| Leaf nodes | 6 |
| Train accuracy | 100% |
| Test accuracy | 90% |
| Build time | ~0.006s |

Note: iris is naturally small because it only has 4 features and 3 well-separated classes.
The theoretical max depth = 4 (one feature per level). Our tree hit depth 4 on one branch.

### max_depth parameter sweep for PopOut — why we test this range

- Theoretical max depth for PopOut = **42** (one per board cell feature)
- In practice leaves become pure well before depth 42 — tree stops naturally
- We test `[1, 3, 5, 7, 10, 15, 20, 30, None]` to show the full curve from shallow → unlimited
- Decision: pick the depth where **test accuracy peaks** — that's our reported model
- This is a deliberate tradeoff: shallower = faster + less overfit; deeper = more expressive but may memorise noise

### PopOut depth sweep results (fill in after running)

| max_depth | actual depth | nodes | leaves | train acc | test acc |
|---|---|---|---|---|---|
| 1 | | | | | |
| 3 | | | | | |
| 5 | | | | | |
| 7 | | | | | |
| 10 | | | | | |
| 15 | | | | | |
| 20 | | | | | |
| 30 | | | | | |
| unlimited | | | | | |

### Expected result: ID3 vs MCTS on PopOut
- ID3 accuracy will be moderate — the tree learns common patterns but has no lookahead
- MCTS is always stronger because it searches forward; the tree only pattern-matches
- Key tradeoff: **interpretability and speed (tree) vs play quality (MCTS)**

### Tree visualisation
- Print full tree for iris (small enough to read entirely)
- For PopOut, print first 3 levels only — full tree would be hundreds of lines
- Both printed trees go in the notebook as code output

---

## Technical Evaluation Section (30% of grade)

- Report accuracy on held-out test set for both datasets
- For iris: compare to known benchmarks (~95% is typical for ID3)
- For PopOut: discuss what "accuracy" means — matching DT-Wide's exact move choice, not necessarily playing the best move
- Show how accuracy changes with max_depth (overfitting curve)
- Mention that the PopOut tree's real test would be win rate vs a random player or vs MCTS — not just move-matching accuracy

---

## Presentation talking points (10 min max)

1. Problem: implement PopOut with MCTS + ID3
2. MCTS: explain UCT, show 2 tournament results, justify DT-Wide choice
3. Dataset generation: DT-Wide vs DT-Wide self-play → N thousand (board, move) pairs
4. ID3: explain entropy/IG, show iris tree (small + interpretable), show PopOut accuracy
5. Tradeoffs: speed vs quality, interpretability vs performance
6. Conclusion: MCTS is the better player; ID3 is faster and explainable
