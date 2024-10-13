import eel
import json 
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

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
                print(f"Ticket parent: {parent_key}")
                
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
