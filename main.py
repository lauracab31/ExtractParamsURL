import threading
import time
import requests
from queue import Queue

#on importe les différentes fonctions de chaque fichier pour les lancer sur différents threads
from webTraffic import web_traffic
from hasDNSRecord import has_DNS_Record
from ageOfDomain import age_of_domain
from adress_bar_based import (
    est_adresse_ip,
    longueur_url,
    contient_arobase,
    contient_sous_domaine,
    has_favicon,
    contient_https
)
from count_external_links import count_external_links
from html_js import has_popup, has_iframe

# Liste d'attente pour les URLs
url_queue = Queue()

# Fonction pour ajouter des URLs à la liste d'attente des URLs à traiter (i.e à encoder)
def add_url_to_queue(url):
    url_queue.put(url)
    print(f"URL ajoutée à la liste d'attente : {url}")

# Fonction principale pour traiter les URLs
def process_urls():
    while not url_queue.empty():
        url = url_queue.get()  # Récupérer une URL de la liste
        print(f"Traitement de l'URL : {url}")
        
        # Dictionnaire pour stocker les résultats pour cette URL
        url_data = {}

        # Liste des threads
        threads = []

        # Fonction pour exécuter une tâche dans un thread et enregistrer le résultat
        def run_task(func, url, key):
            try:
                result = func(url)
                url_data[key] = result
            except Exception as e:
                url_data[key] = f"Erreur : {e}"
        
        # Mapping des fonctions et clés
        tasks = {
            "web_traffic": web_traffic,
            "has_DNS_Record": has_DNS_Record,
            "age_of_domain": age_of_domain,
            "est_adresse_ip": est_adresse_ip,
            "longueur_url": longueur_url,
            "contient_arobase": contient_arobase,
            "contient_sous_domaine": contient_sous_domaine,
            "has_favicon": has_favicon,
            "contient_https": contient_https,
            "count_external_links": count_external_links,
            "has_popup": has_popup,
            "has_iframe": has_iframe,
        }

        # Créer et démarrer les threads
        for key, func in tasks.items():
            thread = threading.Thread(target=run_task, args=(func, url, key))
            threads.append(thread)
            thread.start()

        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()

        # Afficher les résultats pour l'URL
        print(f"Résultats pour {url} : {url_data}")

        # Indiquer que le traitement de cette URL est terminé
        url_queue.task_done()

        #Envoyer les résultats du traitement à l'orchestrateur
        send_results_to_orchestrator(url, url_data)

# Fonction pour envoyer les résultats à l'orchestrateur (exemple)
def send_results_to_orchestrator(url, data):
    orchestrator_endpoint = "http://orchestrator.example.com/receive_data"
    payload = {
        "url": url,
        "data": data
    }
    try:
        response = requests.post(orchestrator_endpoint, json=payload)
        response.raise_for_status()  # Lève une exception si la requête a échoué
        print(f"Résultats envoyés avec succès pour {url}. Réponse : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi des résultats pour {url} : {e}")

# Exemple d'utilisation à mettre dans le main
from orchestrator_utils import send_results_to_orchestrator

# Exemple d'utilisation
url = "http://example.com"
data = {"key": "value"}
send_results_to_orchestrator(url, data)

if __name__ == "__main__":
    # Ajouter des URLs à la liste d'attente
    urls_from_orchestrator = [
        "http://example.com",
        "http://test.com",
        "http://sample.org"
    ]
    for url in urls_from_orchestrator:
        add_url_to_queue(url)

    # Traiter les URLs
    process_urls()
