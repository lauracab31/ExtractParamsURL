from threadsManager import process_url()

# test en local
#url = "http://example.com"
#data = {"key": "value"}
#data=process_url(url, data)

if __name__ == "__main__":
    try:
        # Ajouter des URLs à la liste d'attente
        #urls_from_orchestrator = [
            #"http://example.com",
            #"http://test.com",
            #"http://sample.org"
        #]
        #for url in urls_from_orchestrator:
            #add_url_to_queue(url)

        # Traiter les URLs
        process_url()

        # Attendre que toutes les tâches soient terminées
        #url_queue.join()

    except Exception as e:
        print(f"Erreur inattendue : {e}")
