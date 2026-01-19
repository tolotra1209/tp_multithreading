#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from manager import QueueClient
from task import Task


class Proxy(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.client = QueueClient()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Récupère une tâche de la file d'attente des tâches"""
        try:
            # Récupérer une tâche de la file d'attente
            task_json = self.client.task_queue.get()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # Envoyer la tâche au client HTTP
            self.wfile.write(task_json.encode("utf-8"))
            
        except Exception as e:
            self.send_error(500, f"Erreur lors du GET: {str(e)}")

    def do_POST(self):
        """Envoie un résultat à la file d'attente des résultats"""
        try:
            content_length = int(self.headers.get("content-length", 0))
            if content_length == 0:
                self.send_error(400, "Body manquant")
                return
                
            # Lire les données JSON
            content = self.rfile.read(content_length)
            task_data = content.decode("utf-8")
            
            # Ajouter le résultat à la file d'attente
            self.client.result_queue.put(task_data)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # Répondre avec un accusé de réception
            response = json.dumps({"status": "ok", "message": "Résultat reçu"})
            self.wfile.write(response.encode("utf-8"))
            
        except json.JSONDecodeError:
            self.send_error(400, "JSON invalide")
        except Exception as e:
            self.send_error(500, f"Erreur lors du POST: {str(e)}")

    def log_message(self, format, *args):
        """Personnalisation des logs pour plus de clarté"""
        print(f"[Proxy] {args[0]} {args[1]} {args[2]}")


def run(server_class=HTTPServer, handler_class=Proxy, port=8000):
    """Lance le serveur proxy HTTP"""
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Proxy HTTP démarré sur le port {port}")
    print(f"URL: http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
