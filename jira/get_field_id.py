from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
import json



load_dotenv()
# Configuration
api_token = os.getenv("JIRA_TOKEN")
    
jira_url = os.getenv("JIRA_URL_ACCOUNT")
email = os.getenv("JIRA_MAIL")  # Remplacez par votre email Jira

# Endpoint pour obtenir tous les champs
url = f"{jira_url}/rest/api/3/field"

# Authentification
auth = HTTPBasicAuth(email, api_token)

# En-têtes
headers = {
   "Accept": "application/json"
}

# Faire la requête GET
response = requests.get(url, headers=headers, auth=auth)
FieldSearch="etat"
# Vérifier si la requête a réussi
if response.status_code == 200:
    # Charger les données JSON
    fields = json.loads(response.text)
    
    # Rechercher le champ 'Entreprise'
    field = next((field for field in fields if field['name'].lower() == FieldSearch), None)
    
    if field:
        print(f"Le champ {FieldSearch} a été trouvé :")
        print(f"ID : {field['id']}")
        print(f"Nom : {field['name']}")
        print(f"Type : {field['schema']['type']}")
    else:
        print(f"Le champ {FieldSearch} n'a pas été trouvé.")
        print("Voici tous les champs personnalisés trouvés :")
        for field in fields:
            if field['custom']:
                print(f"ID : {field['id']}, Nom : {field['name']}")
else:
    print(f"La requête a échoué avec le code d'état : {response.status_code}")
    print(f"Message d'erreur : {response.text}")
