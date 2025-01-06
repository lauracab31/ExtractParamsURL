import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


def est_adresse_ip(url):
    """
    Détermine si une URL contient une adresse IP (IPv4 ou IPv6).
    Retourne 1 si c'est une IP, -1 si ce n'est pas une IP, 0 en cas d'erreur.
    """
    try:
        parsed_url = urlparse(url)
        host = parsed_url.netloc

        if host.startswith("www."):
            host = host[4:]

        regex_ipv4 = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        regex_ipv6 = re.compile(r'^[0-9a-fA-F:]+$')

        if regex_ipv4.match(host) or regex_ipv6.match(host):
            return 1
        else:
            return -1
    except Exception:
        return 0

def longueur_url(url):
    """
    Calcule et retourne une valeur en fonction de la longueur totale de l'URL :
    -1 : si la longueur est < 54
     0 : si 54 ≤ longueur ≤ 75
     1 : si longueur > 75
    """
    try:
        # Calculer la longueur totale de l'URL
        longueur = len(url)
        
        # Vérifier la plage de longueur et retourner la valeur correspondante
        if longueur < 54:
            return -1
        elif 54 <= longueur <= 75:
            return 0
        else:
            return 1
    except Exception as e:
        print(f"Erreur lors du calcul de la longueur de l'URL : {e}")
        return 0  # Retourne 0 en cas d'erreur

def contient_arobase(url):
    """
    Vérifie si l'URL contient un caractère '@'.
    Retourne 1 si '@' est présent, -1 sinon.
    """
    try:
        # Vérifier si le caractère '@' est présent dans l'URL
        return 1 if '@' in url else -1
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return 0  # Retourne 0 en cas d'erreur

def contient_https(url):
    """
    Vérifie si l'URL commence par 'https://'.
    """
    try:
        # Vérifier si l'URL commence par 'https://'
        parsed_url = urlparse(url)
        if parsed_url.scheme == "https":
            print(f"L'URL utilise HTTPS : {url}")
            return 1
        else:
            print(f"L'URL n'utilise pas HTTPS : {url}")
            return -1
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return 0

def contient_sous_domaine(url):
    """
    Vérifie si l'URL contient un sous-domaine.
    """
    try:
        # Extraire le domaine de l'URL
        parsed_url = urlparse(url)
        domaine = parsed_url.netloc

        # Retirer le 'www.' s'il est présent
        if domaine.startswith("www."):
            domaine = domaine[4:]

        # Diviser le domaine en parties (par '.'), un sous-domaine doit avoir plus de 2 parties
        parties_domaine = domaine.split('.')
        
        # Si le domaine a plus de 2 parties, il y a un sous-domaine
        if len(parties_domaine) > 2:
            print(f"L'URL contient un sous-domaine : {url}")
            return 1
        else:
            print(f"L'URL ne contient pas de sous-domaine : {url}")
            return -1

    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return 0




def has_favicon(url):
    """
    Vérifie si l'URL possède un favicon, même si le favicon est hébergé sur un autre domaine.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Effectuer une requête GET pour obtenir le contenu de la page
        response = requests.get(url, headers=headers)
        
        # Vérifier si la requête a réussi
        if response.status_code != 200:
            print(f"Erreur : Impossible d'accéder à l'URL. Code de statut {response.status_code}")
            return False
        
        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Rechercher la balise <link> avec rel="icon" ou rel="shortcut icon"
        favicon = soup.find('link', rel=lambda rel: rel and 'icon' in rel.lower())

        if favicon and 'href' in favicon.attrs:
            # Résoudre l'URL complète si nécessaire
            favicon_url = urljoin(url, favicon['href'])
        else:
            # Vérifier la présence d'un favicon par défaut à /favicon.ico
            favicon_url = urljoin(url, '/favicon.ico')
        
        # Vérifier si l'URL du favicon est accessible
        favicon_response = requests.get(favicon_url, headers=headers, stream=True)
        if favicon_response.status_code == 200:
            print(f"Le favicon de l'URL est disponible ici : {favicon_url}")
            return 1
        else:
            print(f"Le favicon est inaccessible : {favicon_url}")
            return -1

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL : {e}")
        return 0


def check_onmouseover(url):
    """
    Vérifie si la source de la page contient un événement onMouseOver.
    Retourne :
    - 1 si onMouseOver est trouvé.
    - -1 sinon.
    """
    try:
        # Définir un User-Agent pour éviter les restrictions sur certains sites
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Récupérer le contenu de la page
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Erreur : Impossible d'accéder à l'URL. Code de statut {response.status_code}")
            return -1
        
        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Rechercher les balises avec un attribut onMouseOver
        onmouseover_tags = soup.find_all(attrs={"onmouseover": True})
        
        # Vérifier si l'attribut modifie la barre de statut
        for tag in onmouseover_tags:
            if "window.status" in tag['onmouseover'].lower():
                print(f"Événement onMouseOver trouvé modifiant la barre de statut : {tag}")
                return 1
        
        # Aucun onMouseOver modifiant la barre de statut trouvé
        print("Aucun événement onMouseOver modifiant la barre de statut trouvé.")
        return -1
    
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return -1


def count_external_links(url):
    """
    Returns 1 if there are more than 2 external links,
    0 if there are 1 or 2 external links,
    -1 if there are no external links.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Unable to access {url}. Status Code: {response.status_code}")
            return -1
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get all anchor tags (<a>) in the webpage
        links = soup.find_all('a', href=True)
        
        # Count external links
        external_links_count = 0
        for link in links:
            href = link['href']
            
            # Check if the link is external (it does not belong to the same domain)
            parsed_url = urlparse(url)
            parsed_href = urlparse(urljoin(url, href))  # Resolve relative URL
            
            # If the domain is different, it is an external link
            if parsed_url.netloc != parsed_href.netloc:
                external_links_count += 1
        
        # Determine result based on the number of external links
        if external_links_count > 2:
            return 1
        elif external_links_count >= 1:
            return 0
        else:
            return -1
            
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")
        return -1


# Exemples d'utilisation
urls = [
    
    "https://www.marmiton.org/recettes/recette_pate-a-crepes_123erjiotejroigjezufhuzehfozehozeotiezotojti72.aspx",
    "http://93.184.216.34/",
    "https://www.wikipedia.org",
    "https://www.google.com/",
    "https://www.kaggle.com/datasets/nitsey/dataset-phising-website",
    
    "https://github.com/",
   
]

for url in urls:
    
    print(f"\nAnalyse de l'URL : {url}")
    
    print("Adresse IP :", est_adresse_ip(url))

    result = longueur_url(url)
    print(f"URL: {url} -> Résultat: {result}")

    result = contient_arobase(url)
    print(f"URL: {url} -> Résultat: {result}")

    result = contient_https(url)
    print(f"URL: {url} -> Contient https : {result}")

    result = contient_sous_domaine(url)
    print(f"URL: {url} -> Contient sous-domaine : {result}")

    result = has_favicon(url)
    print(f"URL: {url} -> Contient favicon : {result}")

    result = check_onmouseover(url)
    print(f"URL: {url} -> on mouseover : {result}")

    result = count_external_links(url)
    print(f"URL: {url} -> count external links : {result}")










