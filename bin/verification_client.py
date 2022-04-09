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
  
def email_is_valid(email):   
  
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

# -------------2-step-verification
import random
import operator

equation_functions = ["+","-","*","/"]

operatorlookup = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def two_step_verification():

    first_value_of_equation = random.randint(-100,100)
    second_value_of_equation = random.randint(-100,100)
        
    random_operator = random.choice(equation_functions)
    solve_the_value = operatorlookup.get(random_operator)

    answer_key = solve_the_value(first_value_of_equation,second_value_of_equation)

    return first_value_of_equation, random_operator, second_value_of_equation, answer_key


