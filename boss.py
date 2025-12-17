# boss.py
import pickle
import time
from queue_manager import start_manager, stop_manager
from task import Task


class Boss:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.manager = None
        self.task_queue = None
        self.result_queue = None

    def connect(self):
        """Se connecte au manager"""
        self.manager = start_manager(self.host, self.port)
        self.task_queue = self.manager.get_task_queue()
        self.result_queue = self.manager.get_result_queue()
        print("Boss connecté au manager")

    def create_tasks(self, num_tasks=5, size=1000):
        """Crée et envoie des tâches"""
        tasks = []
        for i in range(num_tasks):
            task = Task(f"task_{i:03d}", size=size)
            tasks.append(task)
            # Sérialisation de la tâche
            self.task_queue.put(pickle.dumps(task))
            print(f"Tâche {task.identifier} envoyée (taille: {size}x{size})")
        return tasks

    def collect_results(self, timeout=30):
        """Collecte les résultats des tâches"""
        results = []
        start_time = time.time()

        while (
            len(results) < self.task_queue.qsize() or time.time() - start_time < timeout
        ):
            try:
                if not self.result_queue.empty():
                    result_data = self.result_queue.get(timeout=1)
                    result = pickle.loads(result_data)
                    results.append(result)
                    print(
                        f"Résultat reçu: {result.identifier} "
                        f"(temps: {result.time:.4f}s)"
                    )
            except Exception as e:
                print(f"Erreur lors de la collecte: {e}")
                break

        return results

    def shutdown(self):
        """Arrête le système"""
        if self.manager:
            stop_manager(self.manager)
            print("Boss: système arrêté")


if __name__ == "__main__":
    boss = Boss()

    try:
        boss.connect()

        # Créer des tâches
        tasks = boss.create_tasks(num_tasks=3, size=800)

        # Attendre et collecter les résultats
        print("\nAttente des résultats...")
        results = boss.collect_results(timeout=15)

        # Afficher le résumé
        print("\n=== RÉSUMÉ ===")
        for result in results:
            print(f"{result.identifier}: {result.time:.4f} secondes")

        if results:
            avg_time = sum(r.time for r in results) / len(results)
            print(f"\nTemps moyen: {avg_time:.4f} secondes")

    finally:
        boss.shutdown()
