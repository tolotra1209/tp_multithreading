import numpy as np
import time
import json


class Task:
    def __init__(self, identifier: str, size: int = 1000):
        self.identifier = identifier
        self.size = size
        self.A = np.random.rand(size, size)
        self.B = np.random.rand(size)
        # Initialiser x à None au lieu de zéros
        self.x = None  # Changement ici
        self.time = 0

    def work(self):
        start = time.perf_counter()  # Utiliser perf_counter pour plus de précision
        self.x = np.linalg.solve(self.A, self.B)
        self.time = time.perf_counter() - start

    def to_json(self) -> str:
        data = {
            "identifier": self.identifier,
            "size": self.size,
            "A": self.A.tolist(),
            "B": self.B.tolist(),
            "x": self.x.tolist() if self.x is not None else None,  # Gérer None
            "time": self.time,
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def from_json(text: str) -> "Task":
        data = json.loads(text)

        # Créer une nouvelle instance
        task = Task(identifier=data["identifier"], size=data["size"])

        task.A = np.array(data["A"])
        task.B = np.array(data["B"])
        # Gérer le cas où x peut être None
        if data["x"] is not None:
            task.x = np.array(data["x"])
        else:
            task.x = None
        task.time = data["time"]

        return task

    def __eq__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return False

        # Vérifier les attributs simples
        if self.identifier != other.identifier or self.size != other.size:
            return False

        # Vérifier A et B avec tolérance numérique
        if not np.allclose(self.A, other.A, rtol=1e-10, atol=1e-12):
            return False
        if not np.allclose(self.B, other.B, rtol=1e-10, atol=1e-12):
            return False

        # Vérifier x (peut être None)
        if self.x is None and other.x is None:
            x_equal = True
        elif self.x is None or other.x is None:
            x_equal = False
        else:
            x_equal = np.allclose(self.x, other.x, rtol=1e-10, atol=1e-12)

        if not x_equal:
            return False

        # Vérifier time avec tolérance
        time_equal = abs(self.time - other.time) < 1e-9
        return time_equal
