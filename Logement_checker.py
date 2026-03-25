import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging
from plyer import notification
import traceback

# CONFIG
URL = 'https://trouverunlogement.lescrous.fr/tools/41/search?bounds=2.4130316_48.6485333_2.4705092_48.6109217'
CLASSE_CIBLE = 'SearchResults-desktop fr-h4 svelte-11sc5my'
INTERVALLE = 4 * 60  # 4 min
topic = 'Logement-crous' 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# Chemin vers le fichier log
log_file = "C:/Users/hicha/Documents/Code/Logs/Logement_Crous.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')


def envoie_notification(title, message):
    '''Envoie de notification sur le PC'''
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def notifier(titre, message):
    '''Envoie de notification sur le téléphone'''
    headers = {
        "Title": titre,
        "Content-Type": "charset=utf-8"
    }
    response = requests.post(f"https://ntfy.sh/{topic}", data=message.encode('utf-8'), headers=headers)

    if response.status_code != 200:
        logging.error(f"Erreur ntfy : {response.status_code} - {response.text}")

def verifier_contenu():
    '''Scrapper du site du Crous'''
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(class_=CLASSE_CIBLE)

        if element:
            texte = element.get_text(strip=True)
            print(texte)
            if "Aucun" not in texte:
                print('logement trouvé')
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Contenu trouvé : {texte}")
                logging.info("Envoie d'une notification sur le téléphone")
                notifier(texte, "🔔 Logement détecté !")
                time.sleep(60 * 60)

        else:
            logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Élément non trouvé")

    except Exception as e:
        logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Erreur : {e}")

def surveillance():
    logging.info("Script lancé avec succès.")
    Running = True
    while Running:
        try : 
            verifier_contenu()
            time.sleep(INTERVALLE)
        except Exception as e:
            logging.error("Une erreur est survenue : " + str(e))
            logging.error(traceback.format_exc())
            envoie_notification("Erreur dans le script", str(e))
            Running = False

if __name__ == '__main__':
    surveillance()
