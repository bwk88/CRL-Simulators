import subprocess
from PyQt5.QtWidgets import QCompleter, QSizePolicy

def api_invoke():
    print("API button called")
    subprocess.Popen(["python","/home/Root_ka_home/Downloads/app/dynamic_testing_simulator_7.4.4.1/player/API_Client/sksham_client_API.py"])