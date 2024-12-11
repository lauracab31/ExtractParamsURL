import re
from urllib.parse import urlparse

def est_adresse_ip(url):
    """
    Détermine si une URL contient une adresse IP (IPv4 ou IPv6).
    """
    try:
        # Extraire le netloc (nom d'hôte ou IP) depuis l'URL
        parsed_url = urlparse(url)
        host = parsed_url.netloc

        # Enlever 'www.' s'il est présent
        if host.startswith("www."):
            host = host[4:]

        # Expression régulière pour IPv4
        regex_ipv4 = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        # Expression régulière pour IPv6
        regex_ipv6 = re.compile(r'^[0-9a-fA-F:]+$')

        # Vérifier si le nom d'hôte correspond à IPv4 ou IPv6
        if regex_ipv4.match(host):
            print(f"L'URL contient une adresse IPv4 : {host}")
            return True
        elif regex_ipv6.match(host):
            print(f"L'URL contient une adresse IPv6 : {host}")
            return True
        else:
            print(f"L'URL ne contient pas d'adresse IP : {host}")
            return False
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return False

def longueur_url(url):
    """
    Calcule et affiche la longueur totale de l'URL.
    """
    try:
        # Calculer la longueur totale de l'URL
        longueur = len(url)
        print(f"La longueur de l'URL est : {longueur} caractères")
        return longueur
    except Exception as e:
        print(f"Erreur lors du calcul de la longueur de l'URL : {e}")
        return None

def contient_arobase(url):
    """
    Vérifie si l'URL contient un caractère '@'.
    """
    try:
        # Vérifier si le caractère '@' est présent dans l'URL
        if '@' in url:
            print(f"L'URL contient un '@' : {url}")
            return True
        else:
            print(f"L'URL ne contient pas de '@' : {url}")
            return False
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return False

def contient_https(url):
    """
    Vérifie si l'URL commence par 'https://'.
    """
    try:
        # Vérifier si l'URL commence par 'https://'
        parsed_url = urlparse(url)
        if parsed_url.scheme == "https":
            print(f"L'URL utilise HTTPS : {url}")
            return True
        else:
            print(f"L'URL n'utilise pas HTTPS : {url}")
            return False
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return False

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
            return True
        else:
            print(f"L'URL ne contient pas de sous-domaine : {url}")
            return False

    except Exception as e:
        print(f"Erreur lors de l'analyse de l'URL : {e}")
        return False

# Exemples d'utilisation
urls = [
    "http://192.168.1.1/p@age",
    "https://[2001:0db8::1]/path",
    "https://subdomain.example.com",
    "https://www.example.com",
    "http://127.0.0.1/login",
    "https://256.256.256.256",  # Test invalide
]

for url in urls:
    print(f"\nAnalyse de l'URL : {url}")
    est_adresse_ip(url)
    longueur_url(url)
    contient_arobase(url)
    contient_https(url)
    contient_sous_domaine(url)










