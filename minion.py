import sys

sys.path.append(".")

from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


def main():
    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")

    # Connexion au manager du boss
    manager = QueueManager(address=("localhost", 50000), authkey=b"secret")
    manager.connect()

    tasks = manager.get_task_queue()
    results = manager.get_result_queue()

    print("Minion ready to work")

    while True:
        try:
            task = tasks.get(timeout=5)
            if task is None:
                break
            print(f"Minion processing {task.identifier}")
            identifier, x, exec_time = task.work()
            results.put((identifier, x, exec_time))
        except Exception as e:
            print(f"Minion error: {e}")
            break

    print("Minion finished")


if __name__ == "__main__":
    main()
