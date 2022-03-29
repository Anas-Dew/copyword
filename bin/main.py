import os
from time import sleep
import pyperclip as pc
import pymongo
from clearscreen import clear
from termcolor import cprint
from verification_client import save_logs_on_system
import ast

os.chdir(f"{os.getcwd()}\\copyword\\bin")

DBClient = pymongo.MongoClient("mongodb://localhost:27017")

DB = DBClient['copyword']
userbase = DB['userbase']
existed_account_schema = ""

# -----------------------------------------------------------------------------
def read_existing_login_from_local():

    global existed_account_schema
    try:
        file = open('user_login.file','r')

        login_values_in_raw_format = file.readline()
        login_values_in_dictionary = ast.literal_eval(login_values_in_raw_format)
        
        read_account_schema = {
            "email" : login_values_in_dictionary['email'],
            "name" : login_values_in_dictionary['name'],
            "password" : login_values_in_dictionary['password']
        }
        existed_account_schema = read_account_schema
        email = login_values_in_dictionary['email']

        print(f"\nWelcome, {userbase.find_one({'email' : f'{email}'})['name']}")

        keeping_the_server_updated()

    except:

        print("Hmm... Looks like you're not logged in")
        sleep(1)
        print("\nRedirecting you to login/signup menu...")
        sleep(1)
        clear()
        main_driver()


def create_my_account():

    global existed_account_schema
    print("---> Create New Account\n")

    name = input("Enter Your Name : ")
    email = input("Enter Your Email : ")
    password = input("Create A Password : ")

    new_account_schema = {
        "email" : email,
        "name" : name,
        "password" : password
    }
    
    userbase.insert_one(new_account_schema)
    existed_account_schema = new_account_schema
    save_logs_on_system(existed_account_schema)

    cprint("new account creating done !","green")
    

def user_login():

    global existed_account_schema

    print("---> Login \n")
    
    try:

        email = input("Enter Your Email : ")
        password = input("Enter Your Password : ")
        
        print(f"\n-------> Welcome, {userbase.find_one({'email' : f'{email}'})['name']}")

    except:
        cprint("Account not found !","red")
        print("\nPlease check email or password !!!")
        sleep(3)
        clear()
        user_login()

    existed_account_schema = {
        "email" : email,
        "name" : {userbase.find_one({'email' : f'{email}'})['name']},
        "password" : password
    }
    
    cprint("login success !","green")
    save_logs_on_system(existed_account_schema)
# -----------------------------------------------------------------------------------------

def create_and_update_new_word_instance_on_server():

    new_copied_object = {"clipboard" : f"{pc.paste()}"}
    userbase.find_one_and_update({"email" : existed_account_schema["email"]},{"$set" : new_copied_object})

    
    
def reading_new_clipboard_from_server():

    new_clipboard_object = userbase.find_one({"email" : existed_account_schema["email"]})['clipboard']
    pc.copy(new_clipboard_object)


def keeping_the_server_updated():
    
    cprint("creating object done !","blue")
    cprint("Successfully connected to server !","green")
    sleep(2)
    clear()
    cprint("Press 'Control + C' to logout","yellow")
    try:

        while True:
            create_and_update_new_word_instance_on_server()
            reading_new_clipboard_from_server()
            sleep(2)

    except:
        print("You're logged out of your account")
        os.remove("user_login.file")
        sleep(2)
        clear()
        main_driver()

# ---------------------------------------------------------------------------------------
def main_driver():

    print("CopyWord CLI @Anas-Dew  - 2022")

    try:
        user_choice = int(input("1 - Create New Account\n2 - Login Your Account\n"))
    except:
        print("Choose a right value")
        sleep(1)
        clear()
        main_driver()
    
    if user_choice == 1:
        clear()
        create_my_account()
        keeping_the_server_updated()

    elif user_choice == 2:
        clear()
        user_login()
        keeping_the_server_updated()

    else:
        print("Choose a right value")
        clear()
        main_driver()

if __name__ == "__main__" :

    read_existing_login_from_local()
    # main_driver()

    # create_my_account()
    # user_login()
    


    pass