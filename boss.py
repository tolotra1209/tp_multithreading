import sys

sys.path.append(".")

from multiprocessing.managers import BaseManager
from queue import Queue
from task import Task


class QueueManager(BaseManager):
    pass


def main():
    # Enregistrement des files dans le manager
    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)

    # Création des files
    task_queue = Queue()
    result_queue = Queue()

    # Création du manager sur localhost, port 50000
    manager = QueueManager(address=("", 50000), authkey=b"secret")
    manager.start()
    print("Boss started on port 50000")

    # Récupération des files via le manager
    tasks = manager.get_task_queue()
    results = manager.get_result_queue()

    # Création et envoi de 10 tâches
    for i in range(10):
        t = Task(identifier=f"task-{i}", size=800)
        tasks.put(t)
        print(f"Boss added task {t.identifier} to queue")

    # Récupération des résultats
    for _ in range(10):
        identifier, x, exec_time = results.get()
        print(f"Boss received result from {identifier} in {exec_time:.4f}s")

    # Arrêt du manager
    manager.shutdown()
    print("Boss finished")


if __name__ == "__main__":
    main()
