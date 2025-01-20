import threading
import time
#on importe les différentes fonctions de chaque fichier pour les lancer sur différents threads
from webTraffic import web_traffic
from hasDNSRecord import has_DNS_Record
from ageOfDomain import age_of_domain
import adress_bar_based
from count_external_links import count_external_links
import html_js


# Créer les threads
thread1 = threading.Thread(target=web_traffic, args=("argument1",))
thread2 = threading.Thread(target=has_DNS_Record, args=("argument2"))
thread3 = threading.Thread(target=age_of_domain, args=("argument2"))
thread3 = threading.Thread(target=adress_bar_based.est_adresse_ip, args=("argument2"))
thread3 = threading.Thread(target=adress_bar_based.longueur_url, args=("argument2"))
thread3 = threading.Thread(target=adress_bar_based.contient_arobase, args=("argument2"))
thread3 = threading.Thread(target=adress_bar_based.contient_sous_domaine, args=("argument2"))
thread3 = threading.Thread(target=adress_bar_based.has_favicon, args=("argument2"))
thread3 = threading.Thread(target=adress_bar_based.contient_https, args=("argument2"))
thread3 = threading.Thread(target=count_external_links, args=("argument2"))
thread3 = threading.Thread(target=adress_bar_based.has_favicon, args=("argument2"))






#on lance un compteur pour évaluer le temps de la requête
start = time.perf_counter()

# Lancer les threads avec arguments
thread1.start()
thread2.start()

# Attendre la fin des threads
thread1.join()
thread2.join()

#on évalue le temps qui s'est écoulé
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')



