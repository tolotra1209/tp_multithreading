import unittest
import json
import numpy as np
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

    def test_json_serialization_roundtrip(self):
        # Créer une instance
        original = Task(identifier=42, size=20)
        original.work()  # Remplir x et time

        # Sérialiser en JSON
        json_str = original.to_json()
        self.assertIsInstance(json_str, str)

        # Vérifier que c'est du JSON valide
        parsed = json.loads(json_str)
        self.assertEqual(parsed["identifier"], 42)
        self.assertEqual(parsed["size"], 20)

        # Désérialiser
        restored = Task.from_json(json_str)

        # Vérifier l'égalité
        self.assertEqual(original, restored)

        # Vérifier que la solution est toujours valide
        assert_allclose(restored.a @ restored.x, restored.b, rtol=1e-7, atol=1e-9)

    def test_json_serialization_without_work(self):
        original = Task(identifier=99, size=15)
        # Ne pas appeler work() - x doit rester à zéro

        json_str = original.to_json()
        restored = Task.from_json(json_str)

        self.assertEqual(original, restored)
        self.assertTrue(np.allclose(restored.x, np.zeros(15)))
        self.assertEqual(restored.time, 0.0)

    def test_equality_method(self):
        # Deux tâches identiques
        t1 = Task(identifier=1, size=30)
        t1.work()

        t2 = Task(identifier=1, size=30)
        t2.a = t1.a.copy()  # Même matrice A
        t2.b = t1.b.copy()  # Même vecteur b
        t2.x = t1.x.copy()  # Même solution
        t2.time = t1.time  # Même temps

        self.assertEqual(t1, t2)

        # Deux tâches différentes
        t3 = Task(identifier=2, size=30)
        t3.work()
        self.assertNotEqual(t1, t3)

    def test_equality_with_different_types(self):
        task = Task(identifier=1, size=10)

        # Comparaison avec un string
        self.assertFalse(task == "not a task")

        # Comparaison avec None (corrigé selon PEP 8)
        self.assertFalse(task is None)

        # Comparaison avec un nombre
        self.assertFalse(task == 42)

    def test_json_structure(self):
        task = Task(identifier=7, size=5)
        task.work()

        json_str = task.to_json()
        data = json.loads(json_str)

        # Vérifier tous les champs requis
        required_fields = ["identifier", "size", "a", "b", "x", "time"]
        for field in required_fields:
            self.assertIn(field, data)

        # Vérifier les dimensions
        self.assertEqual(len(data["a"]), 5)  # 5 lignes
        self.assertEqual(len(data["a"][0]), 5)  # 5 colonnes
        self.assertEqual(len(data["b"]), 5)
        self.assertEqual(len(data["x"]), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
