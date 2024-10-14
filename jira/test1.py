from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import psutil
import os
from dotenv import load_dotenv
import time

def lister_chrome():
    # Liste pour stocker les instances de Google Chrome
    chrome_instances = []

    # Parcourir tous les processus en cours
    for process in psutil.process_iter(['name', 'pid']):
        try:
            # Vérifier si le processus est Google Chrome
            if process.info['name'] == 'chrome.exe':
                chrome_instances.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return chrome_instances

def ouvrir_nouvel_onglet(url):
    # Vérifier s'il y a des instances de Chrome
    load_dotenv()
    chrome_instances = lister_chrome()
    if chrome_instances:
        # Ouvrir une nouvelle instance de Chrome
        chrome_path = os.getenv("GOOGLE_CHROME")  # Mettez à jour ce chemin si nécessaire
        service = Service(executable_path=os.getenv("GOOGLE_chromedriver"))  # Mettez à jour le chemin vers ChromeDriver
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        
        # Spécifier le chemin du profil Chrome
        chemin_profil = os.getenv("GOOGLE_PROFIL")
        options.add_argument(f"user-data-dir={chemin_profil}")

        # Ajouter des options pour éviter que Chrome ne se ferme
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")  # Port pour le débogage à distance
        options.add_argument("--disable-infobars")  # Désactiver les infobars
        options.add_argument("--start-maximized")  # Démarrer en mode maximisé
        options.add_argument("--disable-extensions")  # Désactiver les extensions

        driver = webdriver.Chrome(service=service, options=options)

        # Ouvrir l'URL dans un nouvel onglet
        driver.get(url)

        # Attendre que la page se charge
        #time.sleep(3)  # Ajustez le temps si nécessaire

        # Accepter les cookies (ajustez le sélecteur si nécessaire)
        try:
            accept_cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accepter')]")
            accept_cookies_button.click()
        except Exception as e:
            print("Le bouton d'acceptation des cookies n'a pas été trouvé ou une erreur s'est produite :", e)

        # Garder le navigateur ouvert
        input("Appuyez sur Entrée pour fermer le navigateur...")  # Attendre que l'utilisateur appuie sur Entrée
    else:
        print("Aucune instance de Google Chrome en cours.")

# Exemple d'utilisation
ouvrir_nouvel_onglet('https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/174835859W?xtor=AL-406')
