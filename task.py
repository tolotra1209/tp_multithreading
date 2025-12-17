import numpy as np
import time
import json


class Task:
    def __init__(self, identifier: str, size: int = 1000):
        self.identifier = identifier
        self.size = size
        self.A = np.random.rand(size, size)
        self.B = np.random.rand(size)
        self.x = None
        self.time = None

    def work(self):
        start = time.time()
        self.x = np.linalg.solve(self.A, self.B)
        self.time = time.time() - start
        return self.identifier, self.x, self.time

    def to_json(self) -> str:
        data = {
            "identifier": self.identifier,
            "size": self.size,
            "A": self.A.tolist() if self.A is not None else None,
            "B": self.B.tolist() if self.B is not None else None,
            "x": self.x.tolist() if self.x is not None else None,
            "time": self.time,
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def from_json(text: str) -> "Task":
        data = json.loads(text)

        # Créer une nouvelle instance
        task = Task(identifier=data["identifier"], size=data["size"])

        # Restaurer les matrices si elles existent
        if data["A"] is not None:
            task.A = np.array(data["A"])
        if data["B"] is not None:
            task.B = np.array(data["B"])
        if data["x"] is not None:
            task.x = np.array(data["x"])

        task.time = data["time"]
        return task

    def __eq__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return False

        # Comparaison basique
        if self.identifier != other.identifier:
            return False

        if self.size != other.size:
            return False

        # Comparaison des matrices A et B (toujours présentes)
        if not np.allclose(self.A, other.A, rtol=1e-7, atol=0):
            return False

        if not np.allclose(self.B, other.B, rtol=1e-7, atol=0):
            return False

        # Comparaison de x (peut être None)
        if self.x is None and other.x is None:
            pass  # OK
        elif self.x is None or other.x is None:
            return False
        elif not np.allclose(self.x, other.x, rtol=1e-7, atol=0):
            return False

        # Comparaison du temps (peut être None)
        if self.time is None and other.time is None:
            pass  # OK
        elif self.time is None or other.time is None:
            return False
        elif abs(self.time - other.time) > 1e-7:
            return False

        return True
