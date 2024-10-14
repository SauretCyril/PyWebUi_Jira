import webbrowser  # Import the webbrowser module
import os

def open_chrome(url='http://www.google.com'):
    # Ouvre Google Chrome avec l'URL spécifiée
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Update this path if necessary
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(url)

# Exemple d'utilisation
open_chrome()  # Ou
