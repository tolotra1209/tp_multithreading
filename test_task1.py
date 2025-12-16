import time
import numpy as np
import json


class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        # choose the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def to_json(self) -> str:
        """
        Sérialise l'instance Task en chaîne JSON.
        Note: Les tableaux numpy sont convertis en listes Python.
        """
        data = {
            "identifier": self.identifier,
            "size": self.size,
            "a": self.a.tolist(),  # Convertir ndarray en liste
            "b": self.b.tolist(),
            "x": self.x.tolist(),
            "time": self.time,
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def from_json(text: str) -> "Task":
        """
        Désérialise une chaîne JSON en instance Task.
        """
        data = json.loads(text)

        # Créer une instance avec l'identifiant et la taille
        task = Task(identifier=data["identifier"], size=data["size"])

        # Restaurer les données (en convertissant les listes en ndarray)
        task.a = np.array(data["a"])
        task.b = np.array(data["b"])
        task.x = np.array(data["x"])
        task.time = data["time"]

        return task

    def __eq__(self, other: object) -> bool:
        """
        Compare deux instances de Task.
        """
        if not isinstance(other, Task):
            return False

        # Comparer les attributs scalaires
        if (
            self.identifier != other.identifier
            or self.size != other.size
            or self.time != other.time
        ):
            return False

        # Comparer les tableaux numpy avec une tolérance numérique
        tolerance = 1e-10
        if not np.allclose(self.a, other.a, rtol=tolerance, atol=tolerance):
            return False
        if not np.allclose(self.b, other.b, rtol=tolerance, atol=tolerance):
            return False
        if not np.allclose(self.x, other.x, rtol=tolerance, atol=tolerance):
            return False

        return True

    def __repr__(self) -> str:
        return f"Task(id={self.identifier}, size={self.size}, time={self.time:.4f}s)"
