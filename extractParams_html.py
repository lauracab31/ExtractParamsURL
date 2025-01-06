import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin



def has_popup(url):
    response = requests.get(url)

    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Vérifier si le code HTML contient des balises de popup
    popup_keywords = ['popup', 'modal', 'alert', 'dialog']
    popup_found = False

    for keyword in popup_keywords:
        if soup.find_all(attrs={"class": keyword}) or soup.find_all(attrs={"id": keyword}):
            popup_found = True
            print(f"Popup keyword '{keyword}' detected!Popup Detected in HTML!")
            return True

    return popup_found

def has_iframe(url):
    response = requests.get(url)

    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Vérifier si le code HTML contient des balises iframe
    iframes = soup.find_all('iframe')

    if iframes:
        print(f"Found {len(iframes)} iframe(s):")
        for i, iframe in enumerate(iframes, start=1):
            print(f"\nIframe {i}:")
            print(f" - Full Tag: {iframe}")
            print(f" - Source (src): {iframe.get('src', 'No src attribute')}")
            return True
    else:
        return False


def has_rightClick(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # verifier dans le div s'il contient click droit
    overlays = soup.find_all('div', style=lambda value: value and 'pointer-events: none' in value)
    if overlays:
        print("Overlay detected that may block right-click.")
    else:
        print("No overlay detected.")


urls = [

    "https://www.marmiton.org/recettes/recette_pate-a-crepes_12372.aspx",
    "https://www.wikipedia.org",
    "https://www.kaggle.com/datasets/nitsey/dataset-phising-website"

]

for url in urls:
    print(f"\nAnalyse de l'URL : {url}")
    has_popup(url)
    has_iframe(url)
    has_rightClick(url)
