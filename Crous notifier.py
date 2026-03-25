from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from plyer import notification 
import requests
from datetime import datetime

# Config

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}
topic = 'Logement-crous'

INTERVALLE = 20   # 20 secondes
URL = 'https://trouverunlogement.lescrous.fr/tools/41/search?bounds=2.4130316_48.6485333_2.4705092_48.6109217'
# à remplacer par la zone géographique qu'on vise (optenable grâce à la map sur le site puis prendre url)

classe_nb_logement = 'SearchResults-desktop fr-h4 svelte-11sc5my'
classe_annonces = "fr-card__title"
classe_connection = "fr-btn fr-icon-account-line"

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
})
PROFILE_PATH = "C:/Users/user/AppData/Local/Google/Chrome/User Data"
# remplacer "user" par "le nom du dossier de la session de l'utilisateur"
log_file = "./logs/logement_crous.log"
# remplacer par le chemin d'accès du fichier de log
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')


cookies = {
    'name': 'PHPSESSID',
    'value': 'valeur_du_cookie_de_la_session',
}

# fonctions

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

def Est_connecte(driver):
    try:
        element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".fr-btn.fr-icon-account-line")))
        texte = element.text.strip()

        if texte == "Identification":
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO : L'utilisateur n'est plus connecté au Crous")
            return False
        return True
    except Exception:
        return False

def passage(driver):
    try:
        # Attendre que le lien "Passer à la recherche de logements" soit visible
        lien = driver.find_element(By.NAME, "searchSubmit")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", lien)
        # Cliquer sur le lien
        lien.click()
        # Attendre un peu pour observer ou pour que la navigation se fasse
        time.sleep(2)

    except Exception as e:
        #logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Erreur lors du clic sur le lien")
        pass

def checker():
    # Options du navigateur
    
    CHEMIN_PROFIL = "C:\Profile 1"
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f"--user-data-dir={CHEMIN_PROFIL}") 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(f"user-agent={HEADERS['User-Agent']}")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #chrome_options.add_argument("--no-sandbox")
    last_run = datetime.now()
    
    # Lancer Selenium
    driver = webdriver.Chrome(options=chrome_options)

    # Charger le domaine du cookie (exemple : CROUS)
    driver.get(URL)  # ou l'URL racine du domaine

    # Ajouter le cookie une fois sur le bon domaine
    driver.add_cookie({
        "name": cookies['name'],
        "value": cookies['value'],
       })
    
    driver.get(URL)
    
    # on attend que la page charge
    time.sleep(2)  
    # on vérifie la connection 
    
    print("l'utilisateur est-il connecté ? :", Est_connecte(driver))

    # si pas connecté on demande les cookies et on attend que l'utilisateur les donnes
    
    if not Est_connecte(driver):
        # on attend que l'utilisateur se connecte
        print("Veuillez vous connecter au Crous.")
        logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] L'utilisateur n'est pas connecté, on attend qu'il se connecte.")
        notifier("Connexion requise", "Veuillez remettre les cookies de connexion au Crous pour continuer.")   
        driver.quit()
        time.sleep(60*10)  # Attendre 10 minutes avant de relancer le script

    else : 
        counter = 0 # nb fois qu'on voit une résidence le drageur depuis l'exécution du programme
        testing = True
        while testing:
            
            
                    
            now = datetime.now()
            if (now - last_run).total_seconds() >= 3600:
                notifier("le script fonctionne toujours", "pas de soucis en vue, ptet un logement à l'horizon :p")
                last_run = now
                                
            # on passe la page de gestion
            time.sleep(1)  # Attendre que la page se charge complètement
            passage(driver)
            
            # on cherche evry dans les locations
            time.sleep(1)
            try : 
                """search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".PlaceAutocomplete__input.fr-input.fr-mt-1w.fr-mb-2w"))
                )"""
                search_input =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            (By.XPATH, "//input[contains(@class,'PlaceAutocomplete__input') and contains(@class,'fr-input')]")
                            ))

                search_input.clear()
                search_input.send_keys("Evry (91000)")
                # à remplacer par le choix proposé par les suggestions lors de la recherche du logement
                time.sleep(1)  # Attendre que les suggestions apparaissent
            except Exception as e:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Erreur lors de la recherche d'Evry : {e}")
                driver.quit()
                time.sleep(2)
            # Puis attendre et cliquer
            evry_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(text(), 'Évry (91000)')]")
            ))
            evry_option.click()
            time.sleep(2)
            
            # on récupère le nombre de logement
            try:   
                nb_logement = driver.find_element(By.CSS_SELECTOR, ".SearchResults-desktop.fr-h4.svelte-11sc5my").text
            except Exception as e:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Erreur lors de la récupération du nombre de logements : {e}")
                print("erreur nb logement")
                driver.quit()
                time.sleep(2)
            
            if "Aucun" in nb_logement :
                pass
            else:
                # on récupère les annonces
                try : 
                    annonces = driver.find_elements(By.CLASS_NAME, classe_annonces)
                except Exception as e:
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Erreur lors de la récupération des annonces")
                    driver.quit()
                    time.sleep(2)
                for annonce in annonces:
                    try:
                        titre = annonce.text
                        lien = annonce.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        # on vérifie si l'annonce correspond à la résidence souhaitée
                        if "Evry-Dragueur" in titre:
                            # remplacer le nom par celui de la résidence voulue
                            # le nombre de notification est à modifier selon vos préférences
                            envoie_notification("Nouvelle annonce", f"{titre}\n{lien}")
                            notifier("Nouvelle annonce", f"{titre}\n{lien}")
                            time.sleep(0.5)
                            notifier("Nouvelle annonce", f"{titre}\n{lien}")
                            time.sleep(0.5)
                            notifier("Nouvelle annonce", f"{titre}\n{lien}")
                            time.sleep(0.5)
                            notifier("Nouvelle annonce", f"{titre}\n{lien}")
                            time.sleep(0.5)
                            notifier("Nouvelle annonce", f"{titre}\n{lien}")
                            print("dragueur trouvé !")
                            counter += 1
                            time.sleep(5*60)  # Attendre 5 minutes avant de vérifier à nouveau
                            if counter > 30:
                                testing = False
                                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Plus de 30 annonces trouvées, arrêt du script.")

                    except Exception as e:
                        driver.quit()
                        time.sleep(2)  
                        logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Erreur lors du traitement de l'annonce : {e}")
            time.sleep(INTERVALLE)
            driver.refresh()  # Rafraîchir la page pour vérifier les nouvelles annonces

if __name__ == '__main__':
    logging.info("Script lancé avec succès.")
    Running = True
    c = 0
    while Running:
        try: 
            checker()
            time.sleep(60*60)
        except Exception as e:
            logging.error("Une erreur est survenue : " + str(e))
            if c < 15:
                notifier("Erreur détectée", "Une erreur s'est produite dans le script, on redémarre le script")
                c += 1
                if c > 100:
                    Running = False
                    logging.info("Trop d'erreurs, arrêt du script.")
    notifier("Script arrêté", "le script s'est arrêté.")