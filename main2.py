import eel
import sys
from pathlib import Path

# Add the parent directory of the current file to the Python path
sys.path.append(str(Path(__file__).parent))
import  v2.function2 as functions5

eel.init("v2")  # EEL initialization

eel.start("main2.html", size=(1000, 800))  # Starting the App 
