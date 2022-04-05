from time import sleep
from tkinter import Button, Label, Tk, Entry
import ast
import os
import pymongo
from verification_client import save_logs_on_system
import pyperclip as pc


# -------------------------------------some-importrant-variables-and-bases-to-run-application
os.chdir(f"{os.getcwd()}\\copyword\\bin")

DBClient = pymongo.MongoClient("mongodb://localhost:27017")

DB = DBClient['copyword']
userbase = DB['userbase']

existed_account_schema = ""

root = Tk()

root.geometry("350x260")
root.title("CopyWord")
root.configure(background='#1e1e21')
root.resizable('False','False')

main_header_title = Label(root,text="CopyWord PC Client",bg="#1e1e21",fg="White",font="sans 14").pack(pady=10)

status_bar = Label(text="Anas-Dew", bg="Black", fg="White", font="sans 9")
status_bar.pack(side="bottom",fill="x")


# -------------------------------------------------------------app-initialization-function
def read_existing_login_from_local():
    status_bar['text'] = "Loading..."
    
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
        
        
        status_bar['text'] = "Login Succees"
        status_bar['bg'] = "#03700c"
        
        keeping_the_server_updated()
        app_screens("LOGOUT")

    except:
        status_bar['text'] = "You're logged out !!!"
        status_bar['bg'] = "#70030a"
        app_screens("LOGIN")

# ------------------------------------------------------------buttons-of-each-application


logout_button = Button(root, text="Logout", width=25, height=1,command=lambda: log_out_of_account(), activeforeground="white", activebackground="#383838")
I_dont_have_account = Button(root, text="I don't have account", width=25, height=1,command=lambda: app_screens("SIGNUP"), activeforeground="white", activebackground="#383838")
    
login = Button(root, text="Login", width=25, height=1,command=lambda: user_login(), activeforeground="white", activebackground="#383838")
signup = Button(root, text="Create New Account", width=25, height=1,command=lambda: create_my_account(), activeforeground="white", activebackground="#383838")
back_to_previous_menu = Button(root,command=lambda: app_screens("LOGIN"), text="Back", width=25, height=1, activeforeground="white", activebackground="#383838")

# ---------------------
signed_as_user_name_shown_on_screen = Label(root,text=f'Welcome back',bg="#1e1e21",fg="White",font="sans 14")
inner_notification_bar = Label(text="Account Already Exists!", bg="Black", fg="White", font="sans 9")
# ---------------------

user_name = Entry(root, width=30, bg="#383838", fg="White")
user_name.insert(0, 'Name')

email = Entry(root, width=30, bg="#383838", fg="White")
email.insert(0, 'Email')

password = Entry(root, width=30, bg="#383838", fg="White")
password.insert(0, 'Password')

# ----------------------------------------------------------------logic-functions

def user_login():
    global existed_account_schema
    try:
        
        login_creds = {"email" : f"{email.get()}"}
        
        existed_account_schema = {
                "email" : email.get(),
                "name" : {userbase.find_one({'email' : f'{email.get()}'})['name']},
                "password" : password.get()
            }

        if password.get() == userbase.find_one(login_creds)['password'] :

            save_logs_on_system(existed_account_schema)
            keeping_the_server_updated()
            app_screens("LOGOUT")

        else:
            app_screens("ERROR")

    except:
        app_screens("ERROR")
        
# ------------

def create_my_account():
    global existed_account_schema

    try:
        new_account_schema = {
            "email" : email.get(),
            "name" : user_name.get(),
            "password" : password.get()
        }

        if userbase.find_one({"email" : f"{new_account_schema['email']}"}) : #------account-already-found-error
            if inner_notification_bar.pack(side="bottom",fill="x"):
                pass
            else:
                inner_notification_bar.pack(side="bottom",fill="x")
                inner_notification_bar.after(7000,inner_notification_bar.destroy)

        else: #if-account-available-then-create-on-server-and-run-server

            if password.get() != "" or "Password" :

                existed_account_schema = new_account_schema
                userbase.insert_one(existed_account_schema)
                save_logs_on_system(existed_account_schema)
                keeping_the_server_updated()

                app_screens("LOGOUT")

            else:
                app_screens("NEW_AC_ERROR")

    
    except:
        pass


def log_out_of_account():
    os.remove("user_login.file")
    app_screens("LOGIN")
# -------------------------------------------------------all-app-screens-of-application

def app_screens(auth_method:str):

    global existed_account_schema
            

    if auth_method == "LOGIN" : #---------login-screen

        status_bar['text'] = "You're logged out !!!"
        status_bar['bg'] = "#70030a"

        user_name.pack_forget()
        signup.pack_forget()
        back_to_previous_menu.pack_forget()

        signed_as_user_name_shown_on_screen.pack_forget()
        logout_button.pack_forget()

        email.pack(pady=3)
        password.pack(pady=3)
        
        login.pack(padx=2, pady=7)
        I_dont_have_account.pack()
        

    elif auth_method == "SIGNUP" : #---------sign-up-screen

        login.pack_forget()
        I_dont_have_account.pack_forget()

        sleep(0.2)

        user_name.pack(pady=3)
        signup.pack(padx=2, pady=7)
        back_to_previous_menu.pack()

    elif auth_method == "LOGOUT" : #---------screen-after-account-has-logged-in
    
        email.pack_forget()
        password.pack_forget()        

        login.pack_forget()
        I_dont_have_account.pack_forget()

        user_name.pack_forget()
        signup.pack_forget()
        back_to_previous_menu.pack_forget()

        signed_as_user_name_shown_on_screen.pack(pady=10)
        logout_button.pack(padx=2, pady=7)

        status_bar['text'] = "Login Succees"
        status_bar['bg'] = "#03700c"
        signed_as_user_name_shown_on_screen['text'] = f'Welcome, {(list(existed_account_schema["name"]))[0]}'
        signed_as_user_name_shown_on_screen['fg'] = 'white'

    elif auth_method == "ERROR" : #---------screen-if-there-is-any-issue

        login.pack_forget()
        email.pack_forget()
        password.pack_forget()
        I_dont_have_account.pack_forget()

        signed_as_user_name_shown_on_screen.pack(pady=40)

        signed_as_user_name_shown_on_screen['text'] = 'Invalid Email or Password !'
        signed_as_user_name_shown_on_screen['fg'] = 'red'
        status_bar['text'] = "Try Again.."
        status_bar['bg'] = "#70030a"

        back_to_previous_menu.pack()
    
    elif auth_method == "NEW_AC_ERROR" :
        inner_notification_bar.pack(side="bottom",fill="x")
        inner_notification_bar['text'] = "Password cannot be empty !"
        inner_notification_bar.after(5000,inner_notification_bar.destroy)
    else:
        read_existing_login_from_local()

# --------------------------------------------------------------mongodb-server-functions
def create_and_update_new_word_instance_on_server(): #----main-server-driver

    new_copied_object = {"clipboard" : f"{pc.paste()}"}

    userbase.find_one_and_update({"email" : existed_account_schema["email"]},{"$set" : new_copied_object})
    reading_new_clipboard_from_server()
   
    
def reading_new_clipboard_from_server(): #----reading-letest-value-from-server-if-it-comes-from-another-linked-device

    new_clipboard_object = userbase.find_one({"email" : existed_account_schema["email"]})['clipboard']
    pc.copy(new_clipboard_object)

def keeping_the_server_updated(): #----keeping-the-loop-running-so-that-values-got-updated-in-secs
    
        create_and_update_new_word_instance_on_server()    
        root.after(1234,keeping_the_server_updated) #1234-is-in-mili-seconds

# -------------------------main-function


if __name__ == "__main__":
    read_existing_login_from_local()

    root.mainloop()
