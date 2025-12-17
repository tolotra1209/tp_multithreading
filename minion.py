# minion.py
import pickle
from queue_manager import start_manager, stop_manager


class Minion:
    def __init__(self, minion_id, host="localhost", port=5000):
        self.minion_id = minion_id
        self.host = host
        self.port = port
        self.manager = None
        self.task_queue = None
        self.result_queue = None
        self.running = False

    def connect(self):
        """Se connecte au manager"""
        self.manager = start_manager(self.host, self.port)
        self.task_queue = self.manager.get_task_queue()
        self.result_queue = self.manager.get_result_queue()
        print(f"Minion {self.minion_id} connecté")

    def work(self):
        """Exécute les tâches de la queue"""
        self.running = True
        print(f"Minion {self.minion_id} commence à travailler")

        while self.running:
            try:
                # Récupérer une tâche avec timeout
                task_data = self.task_queue.get(timeout=2)

                # Désérialiser et exécuter la tâche
                task = pickle.loads(task_data)
                print(f"Minion {self.minion_id} exécute {task.identifier}")

                # Travailler sur la tâche
                task.work()

                # Envoyer le résultat
                result_data = pickle.dumps(task)
                self.result_queue.put(result_data)
                print(
                    f"Minion {self.minion_id} a terminé {task.identifier} "
                    f"en {task.time:.4f}s"
                )

            except Exception as e:
                # Timeout normal ou autre erreur
                if "timeout" not in str(e).lower():
                    print(f"Minion {self.minion_id} erreur: {e}")

    def stop(self):
        """Arrête le minion"""
        self.running = False
        print(f"Minion {self.minion_id} arrêté")

    def run(self):
        """Lance le minion"""
        try:
            self.connect()
            self.work()
        except KeyboardInterrupt:
            print(f"\nMinion {self.minion_id} interrompu")
        except Exception as e:
            print(f"Minion {self.minion_id} erreur: {e}")
        finally:
            self.stop()
            if self.manager:
                stop_manager(self.manager)


if __name__ == "__main__":
    import sys

    # Récupérer l'ID du minion depuis les arguments
    minion_id = "minion_01"
    if len(sys.argv) > 1:
        minion_id = sys.argv[1]

    minion = Minion(minion_id)
    minion.run()
