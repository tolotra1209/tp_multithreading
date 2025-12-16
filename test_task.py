import unittest
from numpy.testing import assert_allclose

from task import Task


class TestTask(unittest.TestCase):
    def test_task_work_solves_linear_system(self):
        # Taille réduite pour un test rapide et déterministe
        size = 10
        task = Task(identifier=1, size=size)

        # Exécuter le calcul
        task.work()

        # Vérifier que A x ≈ b
        assert_allclose(task.a @ task.x, task.b, rtol=1e-7, atol=1e-9)

        # Vérifier que le temps mesuré est positif
        self.assertGreaterEqual(task.time, 0.0)


if __name__ == "__main__":
    unittest.main()
