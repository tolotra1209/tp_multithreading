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
        data = json.loads(text)

        # Créer une instance avec l'identifiant et la taille
        task = Task(identifier=data["identifier"], size=data["size"])

        # Restaurer les données
        task.a = np.array(data["a"])
        task.b = np.array(data["b"])
        task.x = np.array(data["x"])
        task.time = data["time"]

        return task

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        # Comparer les attributs scalaires
        if (
            self.identifier != other.identifier
            or self.size != other.size
            or abs(self.time - other.time) > 1e-12
        ):
            return False

        # Comparer les tableaux numpy avec tolérance numérique
        tolerance = 1e-10
        return (
            np.allclose(self.a, other.a, rtol=tolerance, atol=tolerance)
            and np.allclose(self.b, other.b, rtol=tolerance, atol=tolerance)
            and np.allclose(self.x, other.x, rtol=tolerance, atol=tolerance)
        )
