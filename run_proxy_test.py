import time
import http.client
from multiprocessing import Process
from task import Task
from proxy import run

print("=== Démarrage du proxy ===")

proxy_proc = Process(target=run)
proxy_proc.start()
time.sleep(2)

print("Proxy démarré sur http://localhost:8000")

print("\n=== Test GET ===")
conn = http.client.HTTPConnection("localhost", 8000)
conn.request("GET", "/")
response = conn.getresponse()
print(f"Status: {response.status}")
data = response.read().decode()
print(f"Données: {data[:100]}...")
conn.close()

print("\n=== Test POST ===")
task = Task("http-test", 80)
task.work()
task_json = task.to_json()

conn = http.client.HTTPConnection("localhost", 8000)
conn.request("POST", "/", task_json)
response = conn.getresponse()
print(f"Status: {response.status}")
data = response.read().decode()
print(f"Réponse: {data}")
conn.close()

print("\n=== Arrêt du proxy ===")
proxy_proc.terminate()
proxy_proc.join()
print("Test terminé")
