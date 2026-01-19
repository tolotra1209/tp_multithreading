import unittest
import time
import json
from multiprocessing import Process
import http.client
import socket
from task import Task
from proxy import run
from manager import QueueClient


class TestProxy(unittest.TestCase):
    def setUp(self):
        # Démarrer le serveur
        self.server_proc = Process(target=run)
        self.server_proc.start()
        
        # Attendre que le serveur soit vraiment prêt
        for _ in range(10):  # Essayer pendant 5 secondes max
            try:
                conn = http.client.HTTPConnection("localhost", 8000, timeout=1)
                conn.request("GET", "/health")  # Ajouter une route de santé si possible
                conn.getresponse()
                conn.close()
                break
            except (ConnectionRefusedError, socket.timeout):
                time.sleep(0.5)
        else:
            self.server_proc.terminate()
            self.fail("Server failed to start")
    
    def tearDown(self):
        # Arrêter proprement le serveur
        if self.server_proc.is_alive():
            self.server_proc.terminate()
            self.server_proc.join(timeout=5)
            if self.server_proc.is_alive():
                self.server_proc.kill()
    
    def test_proxy_http(self):
        # Envoyer une tâche via la queue
        client = QueueClient()
        task = Task("proxy-test", 50)
        client.task_queue.put(task.to_json())
        
        # Laisser le temps au proxy de traiter
        time.sleep(0.5)
        
        # Récupérer via HTTP
        conn = http.client.HTTPConnection("localhost", 8000)
        
        # GET pour récupérer une tâche
        conn.request("GET", "/")
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        
        data = response.read().decode()
        received_task = Task.from_json(data)
        self.assertEqual(received_task.identifier, "proxy-test")
        
        # Traiter la tâche
        received_task.work()
        
        # POST pour retourner le résultat
        conn.request("POST", "/", 
                    body=json.dumps(received_task.to_dict()),  # Utiliser to_dict() si disponible
                    headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        
        conn.close()


if __name__ == "__main__":
    unittest.main()
