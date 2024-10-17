import eel
import sys
from pathlib import Path

# Add the parent directory of the current file to the Python path
sys.path.append(str(Path(__file__).parent))
import  v1.function1 as functions5

eel.init("v1")  # EEL initialization

def open_ticket(ticket_url):
    # Appel de la fonction JavaScript pour ouvrir un nouvel onglet
    eel.openNewTicket(ticket_url)  # Appel à la fonction JavaScript

eel.start("main1.html", size=(1000, 800))  # Starting the App 

