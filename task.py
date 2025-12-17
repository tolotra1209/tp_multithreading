import numpy as np
import time
import json


class Task:
    def __init__(self, identifier: str, size: int = 1000):
        self.identifier = identifier
        self.size = size
        self.A = np.random.rand(size, size)
        self.B = np.random.rand(size)
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.time()
        self.x = np.linalg.solve(self.A, self.B)
        self.time = time.perf_counter() - start

    def to_json(self) -> str:
        data = {
            "identifier": self.identifier,
            "size": self.size,
            "A": self.A.tolist(),
            "B": self.B.tolist(),
            "x": self.x.tolist(),
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
        task.x = np.array(data["x"])
        task.time = data["time"]

        return task

    def __eq__(self, other: "Task") -> bool:
        if not isinstance(other, Task):
            return False

        return (
            self.identifier == other.identifier
            and self.size == other.size
            and np.array_equal(self.A, other.A)
            and np.array_equal(self.B, other.B)
            and np.array_equal(self.x, other.x)
            and self.time == other.time
        )
