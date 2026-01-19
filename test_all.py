import unittest
import time
from multiprocessing import Process
from task import Task
from boss import main as boss_main
from minion import main as minion_main


class TestAll(unittest.TestCase):
    def test_task(self):
        t = Task("test", 50)
        t.work()
        self.assertGreater(t.time, 0)

    def test_boss_minion(self):
        boss = Process(target=boss_main)
        minion = Process(target=minion_main)

        boss.start()
        time.sleep(1)
        minion.start()

        boss.join(timeout=5)
        minion.join(timeout=3)

        # Toujours nettoyer les processus
        if boss.is_alive():
            boss.terminate()
        if minion.is_alive():
            minion.terminate()

        boss.join()
        minion.join()


if __name__ == "__main__":
    unittest.main()
