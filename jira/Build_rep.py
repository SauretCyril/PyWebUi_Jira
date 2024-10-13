import requests
import os
from dotenv import load_dotenv
load_dotenv()
# Configuration
tk = os.getenv("JIRA_TOKEN")
jira_url = 'https://sauretcyril-1721475150681.atlassian.net'
ticket_id = 'GOT3-128'
auth = ('sauretcyril@outlook.fr',tk )

# Récupérer les informations du ticket
response = requests.get(f'{jira_url}/rest/api/3/issue/{ticket_id}', auth=auth)

if response.status_code == 200:
    # Extraire l'ID du ticket
    ticket_data = response.json()
    ticket_key = ticket_data['key']

    # Chemin du répertoire local
    directory_path = f'G:/OneDrive/Entreprendre/Actions/{ticket_key}'

    # Vérifier si le répertoire existe
    if not os.path.exists(directory_path):
        # Créer le répertoire
        os.makedirs(directory_path)
        print(f'Répertoire {directory_path} créé.')
    else:
        print(f'Le répertoire {directory_path} existe déjà.')
else:
    print(f'Erreur lors de la récupération du ticket : {response.status_code}')
