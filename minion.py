from task import Task
from queue_manager import QueueManager


def main():
    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")

    try:
        m = QueueManager(address=("localhost", 50000), authkey=b"abc")
        m.connect()

        tq = m.get_task_queue()
        rq = m.get_result_queue()

        while True:
            data = tq.get()
            if data is None:
                break

            task = Task.from_json(data)
            task.work()
            rq.put(task.to_json())
    except Exception as e:
        print(f"Erreur dans le minion: {e}")
        raise


if __name__ == "__main__":
    main()
