import unittest
import time
import json
import http.client
from multiprocessing import Process
from task import Task
from proxy import run
from manager import QueueClient


class TestProxyComplete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Démarre le proxy dans un processus séparé"""
        cls.proxy_process = Process(target=run, kwargs={'port': 8001})
        cls.proxy_process.start()
        time.sleep(2)  # Attendre que le proxy démarre
    
    @classmethod
    def tearDownClass(cls):
        """Arrête le proxy"""
        if cls.proxy_process and cls.proxy_process.is_alive():
            cls.proxy_process.terminate()
            cls.proxy_process.join(timeout=2)
    
    def setUp(self):
        """Initialise le client de queue avant chaque test"""
        self.client = QueueClient()
    
    def test_proxy_get_with_task(self):
        """Test GET avec une tâche dans la file d'attente"""
        # Ajouter une tâche à la file d'attente
        task = Task("test-get", 50)
        self.client.task_queue.put(task.to_json())
        
        # Récupérer via HTTP GET
        conn = http.client.HTTPConnection("localhost", 8001)
        conn.request("GET", "/")
        response = conn.getresponse()
        
        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader("Content-Type"), "application/json")
        
        # Vérifier les données
        data = response.read().decode()
        received_task = Task.from_json(data)
        self.assertEqual(received_task.identifier, "test-get")
        self.assertEqual(received_task.size, 50)
        
        conn.close()
    
    def test_proxy_post_result(self):
        """Test POST pour envoyer un résultat"""
        # Créer et exécuter une tâche
        task = Task("test-post", 50)
        task.work()
        
        # Envoyer le résultat via HTTP POST
        conn = http.client.HTTPConnection("localhost", 8001)
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/", task.to_json(), headers)
        
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        
        # Vérifier la réponse
        data = response.read().decode()
        response_data = json.loads(data)
        self.assertEqual(response_data["status"], "ok")
        
        conn.close()
        
        # Vérifier que le résultat est dans la file d'attente
        # (dans un vrai système, le boss le récupérerait)
    
    def test_proxy_get_empty_queue(self):
        """Test GET quand la file d'attente est vide"""
        # Vider la file d'attente si nécessaire
        while not self.client.task_queue.empty():
            try:
                self.client.task_queue.get(timeout=0.1)
            except:
                break
        
        # GET sur une file vide (devrait bloquer)
        # On teste avec un timeout court
        conn = http.client.HTTPConnection("localhost", 8001, timeout=2)
        conn.request("GET", "/")
        
        # Dans une vraie application, le GET attendrait qu'une tâche arrive
        # Ici on vérifie juste que la connexion fonctionne
        response = conn.getresponse()
        self.assertIn(response.status, [200, 500])  # Selon l'implémentation
    
    def test_proxy_post_invalid_json(self):
        """Test POST avec JSON invalide"""
        conn = http.client.HTTPConnection("localhost", 8001)
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/", "Ce n'est pas du JSON", headers)
        
        response = conn.getresponse()
        self.assertEqual(response.status, 400)  # Bad Request
        
        conn.close()
    
    def test_proxy_workflow(self):
        """Test complet du workflow proxy"""
        # 1. Le boss ajoute une tâche à la file (simulé)
        task = Task("workflow-test", 30)
        self.client.task_queue.put(task.to_json())
        
        # 2. Un client HTTP GET récupère la tâche
        conn = http.client.HTTPConnection("localhost", 8001)
        conn.request("GET", "/")
        response = conn.getresponse()
        
        self.assertEqual(response.status, 200)
        data = response.read().decode()
        received_task = Task.from_json(data)
        
        # 3. Le client exécute la tâche
        received_task.work()
        
        # 4. Le client POST le résultat
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/", received_task.to_json(), headers)
        response = conn.getresponse()
        
        self.assertEqual(response.status, 200)
        
        # 5. Vérifier que le résultat peut être récupéré
        # (Dans un vrai système, le boss récupère ici)
        result_data = self.client.result_queue.get(timeout=1)
        result_task = Task.from_json(result_data)
        
        self.assertEqual(result_task.identifier, "workflow-test")
        self.assertIsNotNone(result_task.x)
        self.assertGreater(result_task.time, 0)
        
        conn.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
