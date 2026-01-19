import unittest
import time
import json
from multiprocessing import Process
from task import Task
from proxy import run
from manager import QueueClient


class TestProxy(unittest.TestCase):
    def test_proxy_http(self):
        server_proc = Process(target=run)
        server_proc.start()
        time.sleep(1)

        client = QueueClient()

        task = Task("proxy-test", 50)
        client.task_queue.put(task.to_json())

        import http.client

        conn = http.client.HTTPConnection("localhost", 8000)
        conn.request("GET", "/")
        response = conn.getresponse()
        data = response.read().decode()
        received_task = Task.from_json(data)

        self.assertEqual(received_task.identifier, "proxy-test")

        received_task.work()

        conn.request("POST", "/", json.dumps(received_task.to_json()))
        response = conn.getresponse()

        conn.close()
        server_proc.terminate()
        server_proc.join()


if __name__ == "__main__":
    unittest.main()
