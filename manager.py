from queue_manager import QueueManager


class QueueClient:
    def __init__(self):
        QueueManager.register("get_task_queue")
        QueueManager.register("get_result_queue")
        self.manager = QueueManager(address=("localhost", 50000), authkey=b"abc")
        self.manager.connect()
        self.task_queue = self.manager.get_task_queue()
        self.result_queue = self.manager.get_result_queue()
