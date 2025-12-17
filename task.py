import numpy as np
import time


class Task:
    def __init__(self, identifier, size=1000):
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
