import eel
import sys
from pathlib import Path

# Add the parent directory of the current file to the Python path
sys.path.append(str(Path(__file__).parent))
import  jira.function5 as functions5

eel.init("jira")  # EEL initialization

eel.start("main5.html", size=(1000, 800))  # Starting the App 
