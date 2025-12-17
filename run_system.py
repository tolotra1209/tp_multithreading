import subprocess
import time
import sys


def run_system():
    # Lancer le boss dans un processus séparé
    boss_proc = subprocess.Popen([sys.executable, "boss.py"])
    time.sleep(2)  # Attendre que le boss soit prêt

    # Lancer deux minions
    minion_procs = []
    for _ in range(2):
        p = subprocess.Popen([sys.executable, "minion.py"])
        minion_procs.append(p)

    # Attendre la fin du boss
    boss_proc.wait()
    print("Boss finished, stopping minions...")

    # Arrêter les minions
    for p in minion_procs:
        p.terminate()
        p.wait()

    print("All processes finished")


if __name__ == "__main__":
    run_system()
