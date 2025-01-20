import threading
import time
#on importe les différentes fonctions de chaque fichier pour les lancer sur différents threads
from webTraffic import web_traffic
from hasDNSRecord import has_DNS_Record
from ageOfDomain import age_of_domain
from adress_bar_based import est_adresse_ip, longueur_url, contient_arobase, contient_sous_domaine, has_favicon, contient_https
from count_external_links import count_external_links
from html_js import has_popup, has_iframe


# Créer les threads
thread1 = threading.Thread(target=web_traffic, args=("argument1",))
thread2 = threading.Thread(target=has_DNS_Record, args=("argument2"))
thread3 = threading.Thread(target=age_of_domain, args=("argument2"))
thread4 = threading.Thread(target=est_adresse_ip, args=("argument2"))
thread5 = threading.Thread(target=longueur_url, args=("argument2"))
thread6 = threading.Thread(target=contient_arobase, args=("argument2"))
thread7 = threading.Thread(target=contient_sous_domaine, args=("argument2"))
thread8 = threading.Thread(target=has_favicon, args=("argument2"))
thread9 = threading.Thread(target=contient_https, args=("argument2"))
thread10 = threading.Thread(target=count_external_links, args=("argument2"))
thread11 = threading.Thread(target=has_popup, args=("argument2"))
thread12 = threading.Thread(target=has_iframe, args=("argument2"))








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



