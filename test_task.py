import unittest
import numpy as np
import json
from numpy.testing import assert_allclose
from task import Task


class TestTask(unittest.TestCase):
    def test_task_work_solves_linear_system(self):
        task = Task("test", size=5)
        task.work()

        # CORRECTION : utiliser A et B (majuscules) au lieu de a et b
        assert_allclose(task.A @ task.x, task.B, rtol=1e-7, atol=1e-9)

    def test_json_serialization_roundtrip(self):
        t1 = Task("json-test", size=10)
        t1.work()

        json_str = t1.to_json()
        restored = Task.from_json(json_str)

        # Vérifier l'égalité
        self.assertEqual(t1, restored)

        # CORRECTION : utiliser A et B (majuscules)
        if restored.x is not None:
            assert_allclose(restored.A @ restored.x, restored.B, rtol=1e-7, atol=1e-9)

    def test_json_serialization_without_work(self):
        t1 = Task("no-work", size=15)
        json_str = t1.to_json()
        restored = Task.from_json(json_str)

        # Avant work(), x devrait être None ou un tableau de zéros selon l'implémentation
        if restored.x is None:
            # Si x est None
            self.assertIsNone(restored.x)
        else:
            # Si x est initialisé à zéros
            self.assertTrue(np.allclose(restored.x, np.zeros(15)))

    def test_equality_method(self):
        t1 = Task("eq-test", size=8)
        t2 = Task("eq-test", size=8)

        # CORRECTION : utiliser A et B (majuscules)
        t2.A = t1.A.copy()  # Même matrice A
        t2.B = t1.B.copy()  # Même matrice B

        # Les tâches devraient être égales
        self.assertEqual(t1, t2)

        # Modifier B pour rendre les tâches différentes
        t2.B[0] += 0.1
        self.assertNotEqual(t1, t2)

    def test_equality_with_different_types(self):
        t1 = Task("type-test", size=5)
        self.assertNotEqual(t1, "not a task")
        self.assertNotEqual(t1, None)
        self.assertNotEqual(t1, 42)

    def test_json_structure(self):
        task = Task("struct-test", size=5)
        task.work()

        json_str = task.to_json()
        data = json.loads(json_str)

        # CORRECTION : utiliser les noms corrects (majuscules)
        expected_fields = ["identifier", "size", "A", "B", "x", "time"]

        for field in expected_fields:
            self.assertIn(field, data)

        # Vérifier les types
        self.assertIsInstance(data["identifier"], str)
        self.assertIsInstance(data["size"], int)
        self.assertIsInstance(data["A"], list)
        self.assertIsInstance(data["B"], list)
        self.assertIsInstance(data["x"], list)
        self.assertIsInstance(data["time"], (float, type(None)))

        # Vérifier les dimensions
        self.assertEqual(len(data["A"]), 5)
        self.assertEqual(len(data["A"][0]), 5)
        self.assertEqual(len(data["B"]), 5)
        self.assertEqual(len(data["x"]), 5)


if __name__ == "__main__":
    unittest.main()
