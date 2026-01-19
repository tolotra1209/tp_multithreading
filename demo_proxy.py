#!/usr/bin/env python
"""
Démonstration complète du système avec proxy HTTP
"""

import time
import json
import http.client
from multiprocessing import Process, Queue
from queue_manager import QueueManager
from task import Task
from proxy import run as run_proxy


def run_queue_manager():
    """Lance le gestionnaire de files d'attente"""
    task_queue = Queue()
    result_queue = Queue()
    
    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)
    
    manager = QueueManager(address=("localhost", 50000), authkey=b"abc")
    server = manager.get_server()
    print("QueueManager démarré sur localhost:50000")
    server.serve_forever()


def add_tasks_to_queue():
    """Ajoute des tâches à la file d'attente (simule le boss)"""
    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")
    
    manager = QueueManager(address=("localhost", 50000), authkey=b"abc")
    manager.connect()
    
    task_queue = manager.get_task_queue()
    
    # Ajouter 3 tâches de tailles différentes
    tasks = [
        Task("small-task", 100),
        Task("medium-task", 200),
        Task("large-task", 300)
    ]
    
    print("Ajout de tâches à la file d'attente:")
    for task in tasks:
        print(f"  - {task.identifier} (taille: {task.size})")
        task_queue.put(task.to_json())
    
    return manager


def process_results(manager):
    """Récupère et affiche les résultats"""
    result_queue = manager.get_result_queue()
    
    print("\nEn attente des résultats...")
    results_received = 0
    
    while results_received < 3:
        try:
            result_data = result_queue.get(timeout=10)
            result_task = Task.from_json(result_data)
            print(f"\nRésultat reçu:")
            print(f"  Tâche: {result_task.identifier}")
            print(f"  Temps d'exécution: {result_task.time:.4f}s")
            print(f"  Taille: {result_task.size}")
            print(f"  Solution calculée: Oui" if result_task.x is not None else "  Solution calculée: Non")
            results_received += 1
        except Exception as e:
            print(f"Erreur: {e}")
            break


def test_http_client():
    """Teste le proxy avec un client HTTP"""
    print("\n" + "="*50)
    print("Test du proxy HTTP")
    print("="*50)
    
    conn = http.client.HTTPConnection("localhost", 8000)
    
    # Test 1: Récupérer une tâche
    print("\n1. Récupération d'une tâche via GET")
    conn.request("GET", "/")
    response = conn.getresponse()
    
    if response.status == 200:
        data = response.read().decode()
        task = Task.from_json(data)
        print(f"   Tâche reçue: {task.identifier}")
        print(f"   Taille: {task.size}")
        
        # Test 2: Exécuter et renvoyer le résultat
        print("\n2. Exécution de la tâche")
        task.work()
        print(f"   Temps d'exécution: {task.time:.4f}s")
        
        print("\n3. Envoi du résultat via POST")
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/", task.to_json(), headers)
        response = conn.getresponse()
        
        if response.status == 200:
            data = response.read().decode()
            result = json.loads(data)
            print(f"   Réponse du serveur: {result['status']}")
        else:
            print(f"   Erreur: {response.status}")
    else:
        print(f"   Erreur GET: {response.status}")
    
    conn.close()


def main():
    """Fonction principale de démonstration"""
    print("="*50)
    print("DÉMONSTRATION DU SYSTÈME AVEC PROXY HTTP")
    print("="*50)
    
    # Démarrer les composants dans des processus séparés
    processes = []
    
    # 1. QueueManager
    print("\n[1/4] Démarrage du QueueManager...")
    qm_process = Process(target=run_queue_manager)
    qm_process.start()
    processes.append(qm_process)
    time.sleep(2)
    
    # 2. Proxy HTTP
    print("[2/4] Démarrage du proxy HTTP...")
    proxy_process = Process(target=run_proxy)
    proxy_process.start()
    processes.append(proxy_process)
    time.sleep(2)
    
    # 3. Ajouter des tâches (simule le boss)
    print("[3/4] Ajout de tâches à la file d'attente...")
    manager = add_tasks_to_queue()
    
    # 4. Tester le proxy HTTP
    print("[4/4] Test du client HTTP...")
    test_http_client()
    
    # 5. Récupérer les résultats
    process_results(manager)
    
    # Nettoyage
    print("\n" + "="*50)
    print("Nettoyage...")
    for process in processes:
        if process.is_alive():
            process.terminate()
            process.join(timeout=1)
    
    print("Démonstration terminée!")


if __name__ == "__main__":
    main()
