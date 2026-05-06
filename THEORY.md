# Markov equivalence of DAGs

## Criterion

For Bayesian networks (belief networks) represented by DAGs, the following theorem
holds.

**Verma-Pearl theorem.** Two DAGs are Markov equivalent if and only if they have:

1. the same skeleton;
2. the same v-structures (also called immoralities).

Here:

- the **skeleton** is the undirected graph obtained from the DAG by forgetting arrow
  directions;
- a **v-structure** is a pattern `i -> k <- j` such that vertices `i` and `j` are
  not adjacent.

This theorem gives a complete and exact test for Markov equivalence, so we do not
need to enumerate conditional independences directly.

## Why this solves the problem

If two DAGs have the same skeleton and the same set of v-structures, then they
encode the same set of conditional independence relations via d-separation.
Therefore they are Markov equivalent.

Conversely, if the skeletons differ, then some pair of variables is adjacent in
one graph and not adjacent in the other, which changes the set of independences.
If the skeletons are the same but the v-structures differ, then collider behavior
differs, so d-separation also differs. Hence the graphs cannot be Markov
equivalent.

So the algorithm is correct:

1. check that both inputs are DAGs;
2. build the skeleton of each graph and compare them;
3. extract all v-structures in each graph and compare them;
4. return `1` iff both comparisons match.

## Complexity

Let `n` be the number of vertices.

- Skeleton comparison takes `O(n^2)`.
- Extracting v-structures takes `O(sum indeg(v)^2)`, which is `O(n^3)` in the
  worst case.

Therefore the whole algorithm runs in polynomial time and is efficient for typical
assignment-sized networks.
