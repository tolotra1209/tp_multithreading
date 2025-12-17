import unittest
import numpy as np
import json
from task import Task


class TestTaskJSONSerialization(unittest.TestCase):
    def test_serialization_basic(self):
        # Créer une tâche
        a = Task(identifier="test-1", size=10)

        # Sérialiser
        json_str = a.to_json()

        # Vérifier que c'est bien du JSON
        import json

        parsed = json.loads(json_str)
        self.assertIn("identifier", parsed)
        self.assertIn("size", parsed)
        self.assertIn("A", parsed)
        self.assertIn("B", parsed)

        # Désérialiser
        b = Task.from_json(json_str)

        # Vérifier l'égalité
        self.assertEqual(a, b)

    def test_serialization_with_solution(self):
        # Créer et exécuter une tâche
        a = Task(identifier="test-2", size=20)
        a.work()  # Calcule x et time

        # Sérialiser
        json_str = a.to_json()

        # Désérialiser
        b = Task.from_json(json_str)

        # Vérifier l'égalité
        self.assertEqual(a, b)

        # Vérifier spécifiquement la solution
        if a.x is not None and b.x is not None:
            np.testing.assert_allclose(a.x, b.x, rtol=1e-7, atol=0)

    def test_equality_with_tolerance(self):
        a = Task(identifier="same", size=5)
        b = Task(identifier="same", size=5)

        # Copier manuellement les matrices (sans recréer de nouvelles aléatoires)
        b.A = a.A.copy()
        b.B = a.B.copy()

        # Ajouter une très petite perturbation
        b.A[0, 0] += 1e-10

        # Les tâches devraient être égales (tolérance dans np.allclose)
        self.assertEqual(a, b)

    def test_inequality(self):
        a = Task(identifier="task1", size=10)
        b = Task(identifier="task2", size=10)  # ID différent

        self.assertNotEqual(a, b)

        # Même ID mais taille différente
        c = Task(identifier="task1", size=15)
        self.assertNotEqual(a, c)

    def test_serialization_roundtrip_multiple(self):
        original = Task(identifier="roundtrip", size=8)
        original.work()

        current = original
        for i in range(3):
            json_str = current.to_json()
            current = Task.from_json(json_str)
            self.assertEqual(original, current)

    def test_json_structure(self):
        task = Task(identifier="json-test", size=3)
        json_str = task.to_json()

        data = json.loads(json_str)

        # Vérifier les types
        self.assertIsInstance(data["identifier"], str)
        self.assertIsInstance(data["size"], int)
        self.assertIsInstance(data["A"], list)
        self.assertIsInstance(data["B"], list)
        self.assertIsNone(data["x"])  # Pas encore calculé
        self.assertIsNone(data["time"])  # Pas encore calculé

        # Vérifier les dimensions
        self.assertEqual(len(data["A"]), 3)  # 3 lignes
        self.assertEqual(len(data["A"][0]), 3)  # 3 colonnes
        self.assertEqual(len(data["B"]), 3)


if __name__ == "__main__":
    unittest.main()
