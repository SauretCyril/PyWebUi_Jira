import eel
import json 
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import psutil

from dotenv import load_dotenv


@dataclass
class Ticket:
    key: str
    summary: str
    entreprise: str
    parent_desc: str
    status: str
    reponse: str
    url_annonce: str  # Ajout du champ url
    url_ticket:str
     
@eel.expose
def get_jira_ticket(jql_query):
    load_dotenv()

    # Configuration
    api_token = os.getenv("JIRA_TOKEN")
    jira_url = os.getenv("JIRA_URL_ACCOUNT")
    auth = (os.getenv("JIRA_MAIL"), api_token)
    # JQL query pour rechercher les tickets
    

    # Endpoint
    search_url = f'{jira_url}/rest/api/3/search'
    params = {
        'jql': jql_query,
        'fields': 'key,summary,customfield_10041,parent,customfield_10038,status'  # Ajout du champ customfield_10041 pour l'URL
    }

    response = requests.get(search_url, auth=auth, params=params)

    if response.status_code == 200:
        search_results = response.json()
        issues = search_results['issues']
        
        print(f"Nombre de tickets trouvés : {len(issues)}")
        
        tickets = []

        for issue in issues:
            ticket_key = issue['key']
            summary = issue['fields']['summary']
            entreprise = issue['fields'].get('customfield_10041')  # Remplacez 'customfield_10000' par l'ID réel
            url_ticket = f"{jira_url}/browse/{ticket_key}"
            """ print(f"Ticket: {ticket_key}")
            print(f"Summary: {summary}")
            print(f"Entreprise: {entreprise}") """
            parent_desc=""
            # Vérifier si le ticket a un parent
            
            if 'parent' in issue['fields']:
                parent_key = issue['fields']['parent']['key']
                print(f"Ticket {ticket_key }")
                
                # Récupérer les détails du ticket parent
                parent_url = f'{jira_url}/rest/api/3/issue/{parent_key}'
                parent_response = requests.get(parent_url, auth=auth)
                
                if parent_response.status_code == 200:
                    parent_data = parent_response.json()
                    parent_description = parent_data['fields'].get('summary', 'Pas de description')
                    #print(f"Description du ticket parent:")
                    parent_desc=parent_description
                
                else:
                    print(f"Erreur lors de la récupération du ticket parent : {parent_response.status_code}")
                    parent_desc=f"erreur = {parent_response.status_code}"
            else:
                ##print("Ce ticket n'a pas de parent.")
                parent_desc="pas de parent"
            
            # Récupérer l'URL du ticket
            url_annonce = issue['fields'].get('customfield_10038', '')  # Remplacez 'customfield_10001' par l'ID réel du champ URL
            
            status=issue['fields'].get('status', '') 
            # Récupérer l'historique des transitions
            
            transitions_url = f'{jira_url}/rest/api/3/issue/{ticket_key}/changelog'
            transitions_response = requests.get(transitions_url, auth=auth)
            reponse=""
            if transitions_response.status_code == 200:
                changelog = transitions_response.json()
                sent_date = None
                for history in changelog['values']:
                    for item in history['items']:
                        if item['field'] == 'status' and item['toString'] == 'Envoyé':
                            sent_date = datetime.fromisoformat(history['created'].replace('Z', '+00:00'))
                            break
                    if sent_date:
                        break
                
                if sent_date:
                    reponse=f"répondu le{sent_date.strftime('%Y-%m-%d %H:%M:%S')}"
                    ##print(f"Date de passage à l'état Envoyé: {sent_date.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    reponse=f"pas encore répondu"
            else:
                reponse=f"Erreur historique {transitions_response.status_code}"
                ##print(f"Erreur lors de la récupération de l'historique du ticket : {transitions_response.status_code}")
            
            ticket = Ticket(
                key=ticket_key,
                summary=summary,
                entreprise=entreprise,
                parent_desc=parent_desc,
                status=status,
                reponse=reponse,
                url_annonce= url_annonce,  # Ajout de l'URL au ticket
                url_ticket = url_ticket
            )
            tickets.append(ticket)
            
            # print("--------------------------------")
            # #print(f"-Ticket: {ticket.key} - {ticket.entreprise} - {ticket.summary} - {ticket.reponse} - {ticket.parent_desc}")
            # print(f"-STATUS {ticket.status['name']}")  # Correction de l'accès à la valeur du statut
            # print("--------------------------------")
        
        # Convertir la liste de tickets en JSON avant de la retourner
        jsonS=json.dumps([ticket.__dict__ for ticket in tickets])
       
        return  jsonS  # Convertir chaque objet Ticket en dictionnaire et en JSON
    else:
        print(f'Erreur lors de la recherche des tickets : {response.status_code}')
        return []

""" entreprise = "GERFLOR"
jql_query = f"Entreprise ~ '{entreprise}' OR summary ~ '{entreprise}'"
tickets = get_jira_ticket(jql_query)

# Vous pouvez maintenant utiliser la collection de tickets
print(f"Nombre total de tickets récupérés : {len(tickets)}") """



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
@eel.expose
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
#ouvrir_nouvel_onglet('https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/174835859W?xtor=AL-406')
