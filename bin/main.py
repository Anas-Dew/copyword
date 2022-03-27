from time import sleep
import pyperclip as pc
import pymongo
from clearscreen import clear

DBClient = pymongo.MongoClient("mongodb://localhost:27017")

DB = DBClient['copyword']
userbase = DB['userbase']
existed_account_schema = ""


def create_my_account():

    global existed_account_schema
    print("\t Create New Account\n")

    name = input("Enter Your Name : ")
    email = input("Enter Your Email : ")

    # if_username_exists_userbase = userbase.find_one({"name" : f"{name}"})['name']

    # if name == if_username_exists_userbase :
    #     print("Username is not Available !! Try Another")
    #     sleep(1)
    #     clear()
    #     create_my_account()

    password = input("Create A Password : ")

    new_account_schema = {
        "email" : email,
        "name" : name,
        "password" : password
    }

    userbase.insert_one(new_account_schema)
    existed_account_schema = new_account_schema
    print("new account creating done !")



def user_login():

    global existed_account_schema

    print("\t Login \n")
    
    try:

        email = input("Enter Your Email : ")
        password = input("Enter Your Password : ")
        
        print(f"\nWelcome, {userbase.find_one({'email' : f'{email}'})['name']}")

    except:
        print("Account not found !")
        print("\nPlease check email or password !!!")
        sleep(1)
        clear()
        user_login()


    existed_account_schema = {
        "email" : email,
        "name" : {userbase.find_one({'email' : f'{email}'})['name']},
        "password" : password
    }

    print("login success !")

def create_and_update_new_word_instance_on_server():

    new_copied_object = {"clipboard" : f"{pc.paste()}"}
    userbase.find_one_and_update({"email" : existed_account_schema["email"]},{"$set" : new_copied_object})

    
    
def reading_new_clipboard_from_server():

    new_clipboard_object = userbase.find_one({"email" : existed_account_schema["email"]})['clipboard']
    pc.copy(new_clipboard_object)


def keeping_the_server_updated():

    print("creating object done !")
    print("Successfully connected to server !")
    while True:
        create_and_update_new_word_instance_on_server()
        reading_new_clipboard_from_server()
        sleep(2)



if __name__ == "__main__" :

    # create_my_account()
    user_login()

    
    keeping_the_server_updated()


    pass