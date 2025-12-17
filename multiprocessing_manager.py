from multiprocessing.managers import BaseManager
from queue import Queue


class QueueManager(BaseManager):
    pass


QueueManager.register("get_task_queue", callable=lambda: task_queue)
QueueManager.register("get_result_queue", callable=lambda: result_queue)

task_queue = Queue()
result_queue = Queue()
