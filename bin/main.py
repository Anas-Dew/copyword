from time import sleep
import pyperclip as pc
import pymongo


DBClient = pymongo.MongoClient("mongodb://localhost:27017")
# DBClient = pymongo.MongoClient("mongodb://127.168.0.1:27017")
DB = DBClient['copyword']
userbase = DB['userbase']
existed_account_schema = ""


def create_my_account():

    name = input("Enter Your Name : ")
    password = input("Create A Password : ")

    new_account_schema = {
        "name" : name,
        "password" : password
    }

    userbase.insert_one(new_account_schema)
    print("new account creating done !")



def user_login():

    global existed_account_schema

    name = input("Enter Your Name : ")
    password = input("Create A Password : ")

    existed_account_schema = {
        "name" : name,
        "password" : password
    }

    print("login success !")

def create_and_update_new_word_instance_on_server():

    new_copied_object = {"clipboard" : f"{pc.paste()}"}
    userbase.find_one_and_update({"name" : existed_account_schema["name"]},{"$set" : new_copied_object})

    print("creating object done !")
    

def reading_new_clipboard_from_server():

    new_clipboard_object = userbase.find_one({"name" : existed_account_schema["name"]})['clipboard']
    pc.copy(new_clipboard_object)


def keeping_the_server_updated():

    while True:
        create_and_update_new_word_instance_on_server()
        reading_new_clipboard_from_server()
        sleep(2)



if __name__ == "__main__" :

    # create_my_account()
    user_login()
    keeping_the_server_updated()
    # reading_new_clipboard_from_server()

    # print(existed_account_schema)
    pass