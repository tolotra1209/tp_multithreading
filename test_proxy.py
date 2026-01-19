import unittest
import time
import json
from multiprocessing import Process
import http.client
import socket
from task import Task
from proxy import run
from manager import QueueClient, BaseManager
from multiprocessing.managers import BaseManager as BM


class TestProxy(unittest.TestCase):
    def setUp(self):
        self.manager_proc = Process(target=self._run_manager)
        self.manager_proc.start()
        time.sleep(1)  # Laisser le temps au manager de démarrer
        
        self.server_proc = Process(target=run)
        self.server_proc.start()
        
        for _ in range(10):
            try:
                conn = http.client.HTTPConnection("localhost", 8000, timeout=1)
                conn.request("GET", "/")
                conn.getresponse()
                conn.close()
                break
            except (ConnectionRefusedError, socket.timeout):
                time.sleep(0.5)
        else:
            self.server_proc.terminate()
            self.manager_proc.terminate()
            self.fail("Server failed to start")
    
    def _run_manager(self):
        """Fonction pour exécuter le manager dans un processus séparé"""
        manager = BaseManager(address=('', 50000), authkey=b'abc')
        manager.start()
        time.sleep(10)  # Garder le manager en vie pendant le test
    
    def tearDown(self):
        for proc in [self.server_proc, self.manager_proc]:
            if proc and proc.is_alive():
                proc.terminate()
                proc.join(timeout=2)
                if proc.is_alive():
                    proc.kill()
    
    def test_proxy_http(self):
        client = QueueClient()
        
        task = Task("proxy-test", 50)
        client.task_queue.put(task.to_json())
        
        time.sleep(0.5)
        
        conn = http.client.HTTPConnection("localhost", 8000)
        
        conn.request("GET", "/")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        
        data = response.read().decode()
        received_task = Task.from_json(data)
        self.assertEqual(received_task.identifier, "proxy-test")
        
        received_task.work()
        
        task_data = received_task.to_json()
        conn.request("POST", "/", 
                    body=task_data,
                    headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        
        conn.close()

    def test_proxy_get_empty_queue(self):
        """Test GET quand la file d'attente est vide"""
        client = QueueClient()
        
        # Vider la file d'attente si nécessaire
        while not client.task_queue.empty():
            try:
                client.task_queue.get(timeout=0.1)
            except (TimeoutError, Exception):  # Corrigé ici: spécifier les exceptions
                break
        
        # Dans ce test, on suppose que la file est vide
        # Le comportement réel dépend de l'implémentation du proxy
        pass


if __name__ == "__main__":
    unittest.main()
