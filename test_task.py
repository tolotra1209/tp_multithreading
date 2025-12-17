import unittest
import numpy as np
import json
from numpy.testing import assert_allclose
from task import Task


class TestTask(unittest.TestCase):
    def test_task_work_solves_linear_system(self):
        task = Task("test", size=5)
        task.work()

        # Vérifier que x n'est plus None après work()
        self.assertIsNotNone(task.x)

        # Vérifier la solution
        Ax = task.A @ task.x
        assert_allclose(Ax, task.B, rtol=1e-7, atol=1e-9)

        # Vérifier que le temps a été mesuré
        self.assertGreater(task.time, 0)

    def test_json_serialization_roundtrip(self):
        t1 = Task("json-test", size=10)
        t1.work()

        json_str = t1.to_json()
        restored = Task.from_json(json_str)

        # Vérifier l'égalité
        self.assertEqual(t1, restored)

        # Vérifier la solution
        if restored.x is not None:
            Ax = restored.A @ restored.x
            assert_allclose(Ax, restored.B, rtol=1e-7, atol=1e-9)

    def test_json_serialization_without_work(self):
        t1 = Task("no-work", size=15)
        json_str = t1.to_json()
        restored = Task.from_json(json_str)

        # Avant work(), x devrait être None
        self.assertIsNone(restored.x)

    def test_equality_method(self):
        # Test 1: Deux tâches identiques après sérialisation
        t1 = Task("eq-test", size=8)
        t1.work()

        # Sérialiser et désérialiser pour obtenir une copie exacte
        json_str = t1.to_json()
        t2 = Task.from_json(json_str)

        # Elles devraient être égales
        self.assertEqual(t1, t2)

        # Test 2: Tâches différentes (identifiant différent)
        t3 = Task("different", size=8)
        t3.A = t1.A.copy()
        t3.B = t1.B.copy()
        t3.work()
        self.assertNotEqual(t1, t3)

        # Test 3: Mêmes matrices mais taille différente
        t4 = Task("eq-test", size=10)
        self.assertNotEqual(t1, t4)

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

        expected_fields = ["identifier", "size", "A", "B", "x", "time"]

        for field in expected_fields:
            self.assertIn(field, data)

        # Vérifier les types
        self.assertIsInstance(data["identifier"], str)
        self.assertIsInstance(data["size"], int)
        self.assertIsInstance(data["A"], list)
        self.assertIsInstance(data["B"], list)
        self.assertIsInstance(data["x"], list)  # Après work(), x est une liste
        self.assertIsInstance(data["time"], (float, int))

        # Vérifier les dimensions
        self.assertEqual(len(data["A"]), 5)
        self.assertEqual(len(data["A"][0]), 5)
        self.assertEqual(len(data["B"]), 5)
        self.assertEqual(len(data["x"]), 5)

    def test_from_json_with_none_x(self):
        """Tester la désérialisation quand x est None dans le JSON"""
        # Créer une tâche sans work()
        task = Task("none-test", size=3)
        json_str = task.to_json()

        # Vérifier que x est null dans le JSON
        data = json.loads(json_str)
        self.assertIsNone(data["x"])

        # Désérialiser
        restored = Task.from_json(json_str)
        self.assertIsNone(restored.x)

    def test_work_modifies_x(self):
        """Vérifier que work() modifie bien x"""
        task = Task("modify-test", size=5)

        # Avant work(), x est None
        self.assertIsNone(task.x)

        # Après work(), x est calculé
        task.work()
        self.assertIsNotNone(task.x)

        # Vérifier que x n'est pas un vecteur de zéros
        self.assertFalse(np.allclose(task.x, np.zeros(5)))

        # Vérifier la solution
        Ax = task.A @ task.x
        assert_allclose(Ax, task.B, rtol=1e-7, atol=1e-9)


if __name__ == "__main__":
    unittest.main()
