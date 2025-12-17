# main.py
"""
Exemple d'exécution du système de multiprocessing
"""

import subprocess
import time
from boss import Boss


def start_minions(num_minions=2):
    """Démarre plusieurs minions en parallèle"""
    processes = []

    for i in range(num_minions):
        minion_id = f"minion_{i + 1:02d}"
        cmd = ["python", "minion.py", minion_id]
        proc = subprocess.Popen(cmd)
        processes.append(proc)
        print(f"Démarrage de {minion_id}")
        time.sleep(0.5)  # Petit délai entre les démarrages

    return processes


def main():
    # Démarrer les minions
    print("=== DÉMARRAGE DU SYSTÈME ===")
    minions = start_minions(num_minions=3)

    # Donner le temps aux minions de se connecter
    time.sleep(2)

    # Lancer le boss
    print("\n=== DÉMARRAGE DU BOSS ===")
    boss = Boss()

    try:
        boss.connect()

        # Créer des tâches
        print("\n=== CRÉATION DES TÂCHES ===")
        tasks = boss.create_tasks(num_tasks=10, size=700)

        # Attendre les résultats
        print("\n=== COLLECTE DES RÉSULTATS ===")
        results = boss.collect_results(timeout=60)

        # Afficher les statistiques
        print("\n=== STATISTIQUES FINALES ===")
        print(f"Tâches créées: {len(tasks)}")
        print(f"Résultats reçus: {len(results)}")

        if results:
            times = [r.time for r in results]
            print(f"Temps min: {min(times):.4f}s")
            print(f"Temps max: {max(times):.4f}s")
            print(f"Temps moyen: {sum(times) / len(times):.4f}s")

    finally:
        # Nettoyage
        print("\n=== ARRÊT DU SYSTÈME ===")
        boss.shutdown()

        # Arrêter les minions
        for minion in minions:
            minion.terminate()
            minion.wait()

        print("Système complètement arrêté")


if __name__ == "__main__":
    main()
