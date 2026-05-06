def _make_binary_matrix(M):
    n = len(M)
    result = []

    for i in range(n):
        if len(M[i]) != n:
            raise ValueError("matrix is not square.")

        row = []
        for j in range(n):
            x = 1 if M[i][j] else 0
            if i == j and x == 1:
                raise ValueError("contains self-loops.")
            row.append(x)
        result.append(row)

    return result


def _skeleton(G):
    n = len(G)
    edges = set()

    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 1 or G[j][i] == 1:
                edges.add((i, j))

    return edges


def _v_structures(G):
    n = len(G)
    skel = _skeleton(G)
    ans = set()

    for child in range(n):
        parents = []
        for i in range(n):
            if G[i][child] == 1:
                parents.append(i)

        for a in range(len(parents)):
            for b in range(a + 1, len(parents)):
                i = parents[a]
                j = parents[b]

                if i < j:
                    pair = (i, j)
                    triple = (i, child, j)
                else:
                    pair = (j, i)
                    triple = (j, child, i)

                if pair not in skel:
                    ans.add(triple)

    return ans


def MarkovEquiv(A, B):
    A = _make_binary_matrix(A)
    B = _make_binary_matrix(B)

    if len(A) != len(B):
        raise ValueError("Adjacency matrices must have the same size.")

    if _skeleton(A) != _skeleton(B):
        return 0

    if _v_structures(A) != _v_structures(B):
        return 0

    return 1
