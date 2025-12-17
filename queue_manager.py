# queue_manager.py
from multiprocessing_manager import QueueManager
from task import Task
import pickle


def start_manager(host="localhost", port=5000, authkey=b"secret"):
    """Démarre le manager de queues"""
    manager = QueueManager(address=(host, port), authkey=authkey)
    manager.start()
    print(f"Manager démarré sur {host}:{port}")
    return manager


def stop_manager(manager):
    """Arrête le manager"""
    manager.shutdown()
    print("Manager arrêté")


if __name__ == "__main__":
    # Exemple d'utilisation
    manager = start_manager()

    # Accéder aux queues
    tasks = manager.get_task_queue()
    results = manager.get_result_queue()

    # Ajouter quelques tâches
    for i in range(3):
        task = Task(f"task_{i}", size=500)
        tasks.put(pickle.dumps(task))
        print(f"Tâche {task.identifier} ajoutée à la queue")

    # Lire les résultats
    while not results.empty():
        result = pickle.loads(results.get())
        print(f"Résultat reçu: {result.identifier}, temps: {result.time:.4f}s")

    stop_manager(manager)
