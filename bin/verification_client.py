# -------------for-saving-login-data-in-local-machine
import os

def save_logs_on_system(login_data):
    # takes login data and 
    # save in current app working directory
    os.chdir(f"{os.getcwd()}")

    with open("user_login.file","w") as f:
        f.write(str(login_data))

# --------------for-validating-if-entered-mail-is-correct-or-not
import re   
  
basic_email_structure = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
  
def email_is_valid(email : str):   
  
    if(re.search(basic_email_structure,email)):   
        return True   
    else:   
        return False
# --------------for-checking-if-internet-is-active-machine
import requests

url = "https://www.google.com"
timeout = 10

def connection_status_on_machine():
    try:
        # requesting URL
        request = requests.get(url, timeout=timeout)
        return True
    
    # catching exception
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

