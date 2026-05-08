[x] Implement HumanPlayer.get_move() function
[x] Change function names and comments to english
[x] Run the game locally
[x] Test game PvB
[x] Choose python library to make tables and graphs of the battle of the mcts versions
[x] Run 1st tournament with 4 MCTS versions
[x] Run 2nd tournament with 4 subversions of DeepThinker model
[x] Run best MCTS version (DT-Wide) vs itself to populate popout_dataset.csv (15k+ rows, 1185 games)
[x] Implement ID3 decision tree from scratch (decision_tree_id3.py)
[x] Verify ID3 on iris dataset (90% test accuracy, tree depth 4, 11 nodes)

[ ] Run ID3 depth sweep on PopOut (run ONCE, results are persisted to CSV)
      → copy the POPOUT block from the bottom of src/decision_tree/decision_tree_id3.py into a notebook cell
      → run from repo root; takes a few minutes (9 trees × 15k rows each)
      → saves id3_popout_results.csv at the repo root — this is the source of truth for all charts
      → fill in the results table in notebook_notes.md once done

[ ] Generate accuracy-vs-depth bar chart (can be re-run any time from saved CSV)
      → venv/bin/python src/decision_tree/visualize_id3.py
      → reads id3_popout_results.csv → saves src/decision_tree/graphs/popout_accuracy_vs_depth.png
      → safe to re-run with different colors/style without re-running the model

[ ] Build Jupyter notebook (see notebook_notes.md for full outline and talking points)
      → Section 1: MCTS — algorithm explanation, tournament results (PNGs in src/mcts_tournament/graphs/), winner
      → Section 2: Iris ID3 — run decision_tree_id3.py __main__ inline, show tree + accuracy
      → Section 3: PopOut ID3 — depth sweep table + bar chart, discuss tradeoffs vs MCTS

[ ] Create presentation slides (PDF, max 10 min)
      → talking points already in notebook_notes.md
