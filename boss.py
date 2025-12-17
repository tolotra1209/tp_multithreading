import time
from multiprocessing import Process
from task import Task
from queue_manager import QueueManager
from base_manager import task_queue, result_queue


def run_server():
    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)
    m = QueueManager(address=("localhost", 50000), authkey=b"abc")
    s = m.get_server()
    s.serve_forever()


def main():
    p = Process(target=run_server)
    p.start()
    time.sleep(1)

    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")
    m = QueueManager(address=("localhost", 50000), authkey=b"abc")
    m.connect()

    tq = m.get_task_queue()
    rq = m.get_result_queue()

    tasks = [Task(f"t{i}", 100) for i in range(3)]

    for task in tasks:
        tq.put(task.to_json())

    for _ in range(2):
        tq.put(None)

    for _ in range(3):
        data = rq.get()
        task = Task.from_json(data)

    p.terminate()
    p.join()


if __name__ == "__main__":
    main()
