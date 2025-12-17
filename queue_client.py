from queue_manager import QueueManager
from base_manager import get_task_queue, get_result_queue


def get_queues():
    QueueManager.register("get_task_queue", callable=get_task_queue)
    QueueManager.register("get_result_queue", callable=get_result_queue)

    manager = QueueManager(address=("localhost", 50000), authkey=b"abc")
    manager.connect()

    task_queue = manager.get_task_queue()
    result_queue = manager.get_result_queue()
    return task_queue, result_queue


if __name__ == "__main__":
    task_queue, result_queue = get_queues()
