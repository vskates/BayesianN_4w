import unittest

from markov_equiv import MarkovEquiv


class MarkovEquivTests(unittest.TestCase):
    def test_equivalent_chains(self) -> None:
        a = [
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0],
        ]
        b = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
        ]

        self.assertEqual(MarkovEquiv(a, b), 1)

    def test_same_skeleton_but_different_v_structure(self) -> None:
        chain = [
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0],
        ]
        collider = [
            [0, 1, 0],
            [0, 0, 0],
            [0, 1, 0],
        ]

        self.assertEqual(MarkovEquiv(chain, collider), 0)

    def test_different_skeletons(self) -> None:
        a = [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        b = [
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0],
        ]

        self.assertEqual(MarkovEquiv(a, b), 0)

    def test_cycle_is_rejected(self) -> None:
        cyclic = [
            [0, 1],
            [1, 0],
        ]
        dag = [
            [0, 1],
            [0, 0],
        ]

        with self.assertRaises(ValueError):
            MarkovEquiv(cyclic, dag)


if __name__ == "__main__":
    unittest.main()
