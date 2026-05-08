"""ID3 decision tree — works for both discrete and continuous features.

Discrete features (PopOut board cells: 0/1/2): split on each unique value.
Continuous features (iris measurements): binary threshold split, threshold
chosen by maximising information gain over all candidate midpoints.
"""

import math
import csv
import random
from collections import Counter


class Node:
    def __init__(self):
        self.feature = None         # feature name to split on (None at leaves)
        self.threshold = None       # float threshold for continuous splits; None for discrete
        self.children = {}          # discrete: {value: Node}; continuous: {'<=': Node, '>': Node}
        self.label = None           # class label at a leaf node (None at internal nodes)
        self.majority_label = None  # fallback if predict hits an unseen feature value


def entropy(labels) -> float:
    """Shannon entropy of a list of class labels. Returns 0.0 for empty or pure input."""
    if not labels:
        return 0.0
    counts = Counter(labels)
    total = len(labels)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def information_gain(data: list[dict], feature: str, label_col: str,
                     threshold: float | None = None) -> float:
    """Information gain of splitting `data` on `feature`.

    threshold=None  → discrete split: one branch per unique feature value.
    threshold=float → binary split: rows where feature <= threshold vs > threshold.
    """
    labels = [row[label_col] for row in data]
    parent_h = entropy(labels)
    n = len(data)

    if threshold is None:
        partitions = {}
        for row in data:
            partitions.setdefault(row[feature], []).append(row[label_col])
        weighted = sum((len(p) / n) * entropy(p) for p in partitions.values())
    else:
        left  = [row[label_col] for row in data if row[feature] <= threshold]
        right = [row[label_col] for row in data if row[feature] >  threshold]
        weighted = (len(left) / n) * entropy(left) + (len(right) / n) * entropy(right)

    return parent_h - weighted


def best_split(data: list[dict], features: list[str], label_col: str,
               numerical_features: set = frozenset()) -> tuple[str, float | None]:
    """Return (feature, threshold) with the highest information gain.

    For numerical features the best threshold is the midpoint between consecutive
    sorted unique values that maximises information gain.
    threshold is None for discrete features.
    """
    best_gain = -1.0
    best_feature = None
    best_threshold = None

    for feature in features:
        if feature in numerical_features:
            values = sorted(set(row[feature] for row in data))
            thresholds = [(values[i] + values[i + 1]) / 2 for i in range(len(values) - 1)]
            for t in thresholds:
                gain = information_gain(data, feature, label_col, threshold=t)
                if gain > best_gain:
                    best_gain, best_feature, best_threshold = gain, feature, t
        else:
            gain = information_gain(data, feature, label_col)
            if gain > best_gain:
                best_gain, best_feature, best_threshold = gain, feature, None

    return best_feature, best_threshold


def _majority(labels: list) -> str:
    """Return the most common label; alphabetical order breaks ties."""
    counts = Counter(labels)
    return min(counts, key=lambda l: (-counts[l], l))


def build_tree(data: list[dict], features: list[str], label_col: str,
               numerical_features: set = frozenset(),
               max_depth: int | None = None, depth: int = 0) -> Node:
    """Recursively build an ID3 decision tree.

    Stopping conditions (produce a leaf):
    - All examples share the same label (pure node).
    - No features left to split on.
    - max_depth reached.
    """
    node = Node()
    labels = [row[label_col] for row in data]
    node.majority_label = _majority(labels)

    # Pure node
    if len(set(labels)) == 1:
        node.label = labels[0]
        return node

    # No features left or depth limit reached
    if not features or (max_depth is not None and depth >= max_depth):
        node.label = node.majority_label
        return node

    feature, threshold = best_split(data, features, label_col, numerical_features)

    if feature is None:
        node.label = node.majority_label
        return node

    node.feature = feature
    node.threshold = threshold

    if threshold is None:
        # Discrete split — remove this feature from future splits on this branch
        remaining = [f for f in features if f != feature]
        partitions = {}
        for row in data:
            partitions.setdefault(row[feature], []).append(row)

        for val, subset in partitions.items():
            node.children[val] = build_tree(
                subset, remaining, label_col, numerical_features, max_depth, depth + 1
            )
    else:
        # Continuous split — feature stays available for deeper splits
        left  = [row for row in data if row[feature] <= threshold]
        right = [row for row in data if row[feature] >  threshold]

        for key, subset in [('<=', left), ('>', right)]:
            if subset:
                node.children[key] = build_tree(
                    subset, features, label_col, numerical_features, max_depth, depth + 1
                )
            else:
                leaf = Node()
                leaf.label = node.majority_label
                node.children[key] = leaf

    return node


def predict(node: Node, example: dict) -> str:
    """Walk the tree and return the predicted class label for `example`."""
    if node.label is not None:
        return node.label

    val = example[node.feature]

    if node.threshold is None:
        child = node.children.get(val)
        if child is None:
            return node.majority_label  # unseen value at test time
        return predict(child, example)
    else:
        key = '<=' if val <= node.threshold else '>'
        return predict(node.children[key], example)


def print_tree(node: Node, indent: int = 0, branch_label: str = "",
               max_print_depth: int | None = None) -> None:
    """Print an indented text representation of the tree.

    max_print_depth limits how many levels to print (useful for large PopOut trees).
    """
    if max_print_depth is not None and indent > max_print_depth:
        print("  " * indent + "...")
        return

    prefix = "  " * indent
    tag = f"[{branch_label}] " if branch_label else ""

    if node.label is not None:
        print(f"{prefix}{tag}→ {node.label}")
        return

    if node.threshold is not None:
        print(f"{prefix}{tag}{node.feature} <= {node.threshold:.3f}?")
        print_tree(node.children.get('<='), indent + 1, "<=", max_print_depth)
        print_tree(node.children.get('>'),  indent + 1, ">",  max_print_depth)
    else:
        print(f"{prefix}{tag}{node.feature}?")
        for val in sorted(node.children.keys(), key=str):
            print_tree(node.children[val], indent + 1, str(val), max_print_depth)


def evaluate(node: Node, test_data: list[dict], label_col: str) -> float:
    """Return accuracy (0.0–1.0) of the tree on `test_data`."""
    if not test_data:
        return 0.0
    correct = sum(1 for row in test_data if predict(node, row) == row[label_col])
    return correct / len(test_data)


# ── Helpers ───────────────────────────────────────────────────────────────────

def train_test_split(data: list[dict], test_ratio: float = 0.2,
                     seed: int = 42) -> tuple[list[dict], list[dict]]:
    """Shuffle data and split into (train, test) sets."""
    data = list(data)
    random.seed(seed)
    random.shuffle(data)
    split = int(len(data) * (1 - test_ratio))
    return data[:split], data[split:]


def load_csv(filepath: str) -> list[dict]:
    """Load a CSV with a header row into a list of dicts."""
    with open(filepath, newline='') as f:
        return list(csv.DictReader(f))


def save_results(results: list[dict], filepath: str) -> None:
    """Save a list of result dicts to a CSV file."""
    if not results:
        return
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


# ── TODO for notebook / coworkers ─────────────────────────────────────────────
#
# IRIS (warm-up, no max_depth needed — tree is naturally small):
#
#   data  = load_csv('datasets/iris-dataset.csv')
#   # Drop the ID column, it's not a feature
#   for row in data: del row['ID']
#   numerical = {'sepallength', 'sepalwidth', 'petallength', 'petalwidth'}
#   # CSV loads everything as strings — cast to float
#   for row in data:
#       for f in numerical: row[f] = float(row[f])
#   features  = [f for f in data[0] if f != 'class']
#   train, test = train_test_split(data, test_ratio=0.2)
#   tree = build_tree(train, features, 'class', numerical_features=numerical)
#   print_tree(tree)
#   print(f"Iris test accuracy: {evaluate(tree, test, 'class'):.2%}")
#
# POPOUT (test several max_depth values, compare accuracy):
#
#   data     = load_csv('popout_dataset.csv')
#   features = [f for f in data[0] if f not in ('game_id', 'move')]
#   # cast board cells to int (CSV loads everything as strings)
#   for row in data:
#       for f in features: row[f] = int(row[f])
#   train, test = train_test_split(data, test_ratio=0.2)
#
#   results = []
#   for depth in [5, 10, 20, None]:
#       tree = build_tree(train, features, 'move', max_depth=depth)
#       acc  = evaluate(tree, test, 'move')
#       results.append({'max_depth': depth, 'test_accuracy': acc})
#       print(f"max_depth={depth}: {acc:.2%}")
#       print_tree(tree, max_print_depth=3)   # print first 3 levels only
#
#   save_results(results, 'id3_popout_results.csv')
#   # Then generate a plot with visualize_id3.py (see that file)
#
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import os, sys, time
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    print("=" * 40)
    print("ID3 demo — Iris dataset")
    print("=" * 40)

    data = load_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'iris-dataset.csv'))
    for row in data:
        del row['ID']

    numerical = {'sepallength', 'sepalwidth', 'petallength', 'petalwidth'}
    features  = [f for f in data[0] if f != 'class']

    # CSV loads everything as strings — cast numerical columns to float
    for row in data:
        for f in numerical:
            row[f] = float(row[f])

    classes = Counter(row['class'] for row in data)
    print(f"\nDataset: {len(data)} examples | {len(features)} features | {len(classes)} classes")
    for cls, count in sorted(classes.items()):
        print(f"  {cls}: {count} examples")

    train, test = train_test_split(data, test_ratio=0.2)
    print(f"\nSplit: {len(train)} train / {len(test)} test (80/20)")

    print("\nBuilding tree...", end=" ", flush=True)
    t0 = time.perf_counter()
    tree = build_tree(train, features, 'class', numerical_features=numerical)
    print(f"done in {time.perf_counter() - t0:.3f}s")

    print("\nDecision tree:")
    print_tree(tree)

    train_acc = evaluate(tree, train, 'class')
    test_acc  = evaluate(tree, test,  'class')
    print(f"\nTrain accuracy: {train_acc:.2%}")
    print(f"Test accuracy:  {test_acc:.2%}")
