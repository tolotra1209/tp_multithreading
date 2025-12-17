import unittest
import numpy as np
from task import Task


class TestMultiprocessingSystem(unittest.TestCase):
    def test_task_work(self):
        t = Task("test", size=10)
        identifier, x, exec_time = t.work()
        self.assertEqual(identifier, "test")
        self.assertIsInstance(x, np.ndarray)
        self.assertGreater(exec_time, 0)
        # Vérification que Ax ≈ B
        Ax = t.A @ x
        np.testing.assert_allclose(Ax, t.B, rtol=1e-7, atol=0)


if __name__ == "__main__":
    unittest.main()
