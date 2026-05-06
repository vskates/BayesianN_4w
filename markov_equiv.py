"""Check Markov equivalence of two belief networks represented as DAGs.

The key theorem used here is the Verma-Pearl characterization:
two DAGs are Markov equivalent if and only if they have

1. the same skeleton (the same undirected edges), and
2. the same v-structures / immoralities i -> k <- j
   where i and j are not adjacent.

The public function follows the assignment name and returns 1 or 0.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations
from typing import Iterable, Sequence

MatrixLike = Sequence[Sequence[int | bool | float]]


def _normalize_matrix(matrix: MatrixLike) -> list[list[int]]:
    """Convert a matrix-like object to a square 0/1 adjacency matrix."""

    rows = [list(row) for row in matrix]
    if not rows:
        return []

    size = len(rows)
    for row in rows:
        if len(row) != size:
            raise ValueError("Adjacency matrix must be square.")

    normalized: list[list[int]] = []
    for i, row in enumerate(rows):
        new_row: list[int] = []
        for j, value in enumerate(row):
            edge = 1 if value else 0
            if i == j and edge:
                raise ValueError("A DAG cannot contain self-loops.")
            new_row.append(edge)
        normalized.append(new_row)

    return normalized


def _is_dag(adj: Sequence[Sequence[int]]) -> bool:
    """Return True if the directed graph is acyclic."""

    n = len(adj)
    indegree = [0] * n
    children: list[list[int]] = [[] for _ in range(n)]

    for parent in range(n):
        for child in range(n):
            if adj[parent][child]:
                indegree[child] += 1
                children[parent].append(child)

    queue = deque(node for node, deg in enumerate(indegree) if deg == 0)
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    return visited == n


def _skeleton(adj: Sequence[Sequence[int]]) -> list[list[int]]:
    """Return the undirected skeleton of a DAG as a 0/1 matrix."""

    n = len(adj)
    skeleton = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if adj[i][j] or adj[j][i]:
                skeleton[i][j] = 1
                skeleton[j][i] = 1

    return skeleton


def _parents_of(adj: Sequence[Sequence[int]], node: int) -> list[int]:
    return [parent for parent in range(len(adj)) if adj[parent][node]]


def _v_structures(adj: Sequence[Sequence[int]]) -> set[tuple[int, int, int]]:
    """Return all v-structures as tuples (min_parent, child, max_parent)."""

    skel = _skeleton(adj)
    v_structures: set[tuple[int, int, int]] = set()

    for child in range(len(adj)):
        parents = _parents_of(adj, child)
        for left, right in combinations(sorted(parents), 2):
            if not skel[left][right]:
                v_structures.add((left, child, right))

    return v_structures


def MarkovEquiv(A: MatrixLike, B: MatrixLike) -> int:
    """Return 1 if DAGs A and B are Markov equivalent, otherwise 0.

    Parameters
    ----------
    A, B:
        Square adjacency matrices. A[i][j] = 1 means i -> j.
        Any non-zero value is treated as an edge.
    """

    adj_a = _normalize_matrix(A)
    adj_b = _normalize_matrix(B)

    if len(adj_a) != len(adj_b):
        raise ValueError("Adjacency matrices must have the same size.")

    if not _is_dag(adj_a) or not _is_dag(adj_b):
        raise ValueError("Both inputs must represent DAGs.")

    same_skeleton = _skeleton(adj_a) == _skeleton(adj_b)
    same_v_structures = _v_structures(adj_a) == _v_structures(adj_b)

    return 1 if same_skeleton and same_v_structures else 0


def markov_equiv(A: MatrixLike, B: MatrixLike) -> bool:
    """Pythonic wrapper around MarkovEquiv."""

    return bool(MarkovEquiv(A, B))

