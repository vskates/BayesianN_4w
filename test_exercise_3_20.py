import unittest

from exercise_3_20 import exercise_3_20_joint, exercise_3_20_marginals, independent


class Exercise320Tests(unittest.TestCase):
    def test_joint_distribution(self):
        joint = exercise_3_20_joint()
        expected = [
            [0.112, 0.448, 0.012, 0.028],
            [0.048, 0.192, 0.006, 0.014],
            [0.0, 0.0, 0.024, 0.056],
            [0.0, 0.0, 0.018, 0.042],
        ]

        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(joint[i][j], expected[i][j])

    def test_marginals(self):
        p_w, p_h = exercise_3_20_marginals()

        expected_w = [0.6, 0.26, 0.08, 0.06]
        expected_h = [0.16, 0.64, 0.06, 0.14]

        for i in range(4):
            self.assertAlmostEqual(p_w[i], expected_w[i])
            self.assertAlmostEqual(p_h[i], expected_h[i])

    def test_not_independent(self):
        joint = exercise_3_20_joint()
        self.assertFalse(independent(joint))


if __name__ == "__main__":
    unittest.main()
