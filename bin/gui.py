from time import sleep
from tkinter import Button, Label, Text, Tk, Entry, Menu, messagebox
import ast
import os
import pymongo
from verification_client import save_logs_on_system, email_is_valid, connection_status_on_machine
import pyperclip as pc
import webbrowser
# -------------------------------------some-importrant-variables-and-bases-to-run-application
os.chdir(f"{os.getcwd()}\\copyword\\bin")

DBClient = pymongo.MongoClient("mongodb://localhost:27017")

DB = DBClient['copyword']
userbase = DB['userbase']
feedback_base = DB['feedback_base']

existed_account_schema = ""

root = Tk()
root.iconbitmap("copyword3_icon.ico")
root.geometry("350x260")
root.title("CopyWord")
root.configure(background='#1e1e21')
root.resizable('False','False')

main_header_title = Label(root,text="CopyWord PC Client",bg="#1e1e21",fg="White",font="sans 14").pack(pady=10)

status_bar = Label(text="Anas-Dew", bg="Black", fg="White", font="sans 9")
status_bar.pack(side="bottom",fill="x")

menubar = Menu(root)
# -------------------------------------------------------------app-initialization-function
def read_existing_login_from_local():
    status_bar['text'] = "Loading..."
    
    global existed_account_schema
    try:
        if connection_status_on_machine() == True :

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
        
        else :
            signed_as_user_name_shown_on_screen.pack()
            signed_as_user_name_shown_on_screen['text'] = 'Connection Error..!'
            
            status_bar['text'] = "No internet connection !"
            status_bar['bg'] = "#70030a"

    except:
        status_bar['text'] = "You're logged out !!!"
        status_bar['bg'] = "#70030a"
        app_screens("LOGIN")

# ------------------------------------------------------------buttons-of-each-application

logout_button = Button(root, text="Logout", width=25, height=1,command=lambda: log_out_of_account(), activeforeground="white", activebackground="#383838")
I_dont_have_account = Button(root, text="I don't have account", width=25, height=1,command=lambda: app_screens("SIGNUP"), activeforeground="white", activebackground="#383838")
    
login = Button(root, text="Login", width=25, height=1,command=lambda: user_login(), activeforeground="white", activebackground="#383838")
signup = Button(root, text="Create New Account", width=25, height=1,command=lambda: create_my_account(), activeforeground="white", activebackground="#383838")
back_to_previous_menu = Button(root,command=lambda: back_to_previous_menu_with(), text="Back", width=25, height=1, activeforeground="white", activebackground="#383838")
submit_here = Button(root, text="Submit", width=25, height=1,command=lambda: post_feedback(), activeforeground="white", activebackground="#383838")
# ---------------------
signed_as_user_name_shown_on_screen = Label(root,text=f'Welcome back',bg="#1e1e21",fg="White",font="sans 14")
inner_notification_bar = Label(text="Anas-Dew", bg="Black", fg="White", font="sans 9")
# ---------------------

user_name = Entry(root, width=30, bg="#383838", fg="White")
user_name.insert(0, 'Name')

email = Entry(root, width=30, bg="#383838", fg="White")
email.insert(0, 'Email')

password = Entry(root, width=30, bg="#383838", fg="White")
password.insert(0, 'Password')

feedback_message = Text(root, width=22, height=5, bg="#383838", fg="White")

# -------------------------------------------------------------menu-functions
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Options', menu=file)

file.add_command(label='Download Update', command=lambda: webbrowser.open_new(
        r"https://github.com/Anas-Dew/copyword"))

file.add_command(label='Feedback', command=lambda: app_screens("FEEDBACK"))


root.config(menu=menubar)
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

        if userbase.find_one({"email" : f"{new_account_schema['email']}"}) or email_is_valid(email.get()) == False : #------account-already-found-error

            app_screens("NEW-AC-ERROR", 'Invalid Email or Password" !')

        else:            
                    existed_account_schema = new_account_schema
                    
                    userbase.insert_one(existed_account_schema)
                    save_logs_on_system(existed_account_schema)
                    keeping_the_server_updated()
                    
                    app_screens("LOGOUT")
                
    
    except:
        app_screens("ERROR")


def log_out_of_account():
    global existed_account_schema
    os.remove("user_login.file")
    existed_account_schema = ""
    app_screens("LOGIN")


def post_feedback():
    feedback_message_schema = {
        "email" : email.get(),
        "feedback" : feedback_message.get(1.0, "end-1c")
    }
    if email_is_valid(email.get()) == True :
            
        feedback_base.insert_one(feedback_message_schema)
        messagebox.showinfo("Feedback", "Feedback has been recorded")

    else :
        messagebox.showerror("Feedback", "Email is invalid")

def back_to_previous_menu_with() :

    if existed_account_schema == "":

        app_screens("LOGIN")

    else :

        app_screens("LOGOUT")

# -------------------------------------------------------all-app-screens-of-application

def app_screens(auth_method : str, notification_text : str = None):

    global existed_account_schema
            

    if auth_method == "LOGIN" : #---------login-screen

        status_bar['text'] = "You're logged out !!!"
        status_bar['bg'] = "#70030a"

        inner_notification_bar.pack_forget()
        user_name.pack_forget()
        signup.pack_forget()
        back_to_previous_menu.pack_forget()
        feedback_message.pack_forget()
        signed_as_user_name_shown_on_screen.pack_forget()
        logout_button.pack_forget()
        submit_here.pack_forget()

        email.pack(pady=3)
        password.pack(pady=3)
        
        login.pack(padx=2, pady=7)
        I_dont_have_account.pack()
        

    elif auth_method == "SIGNUP" : #---------sign-up-screen

        login.pack_forget()
        I_dont_have_account.pack_forget()
        feedback_message.pack_forget()
        submit_here.pack_forget()
        sleep(0.2)

        user_name.pack(pady=3)
        signup.pack(padx=2, pady=7)
        
        back_to_previous_menu.pack()


    elif auth_method == "LOGOUT" : #---------screen-after-account-has-logged-in
    
        email.pack_forget()
        password.pack_forget()        
        inner_notification_bar.pack_forget()
        login.pack_forget()
        I_dont_have_account.pack_forget()
        feedback_message.pack_forget()
        user_name.pack_forget()
        signup.pack_forget()
        back_to_previous_menu.pack_forget()
        submit_here.pack_forget()

        signed_as_user_name_shown_on_screen.pack(pady=10)
        logout_button.pack(padx=2, pady=7)

        status_bar['text'] = "Login Succees"
        status_bar['bg'] = "#03700c"
        signed_as_user_name_shown_on_screen['text'] = f'Welcome, {(list(existed_account_schema["name"]))[0]}'
        signed_as_user_name_shown_on_screen['fg'] = 'white'

    elif auth_method == "ERROR" : #---------screen-if-there-is-any-issue
        feedback_message.pack_forget()
        user_name.pack_forget()
        login.pack_forget()
        email.pack_forget()
        password.pack_forget()
        I_dont_have_account.pack_forget()
        inner_notification_bar.pack_forget()
        signed_as_user_name_shown_on_screen.pack(pady=40)
        signup.pack_forget()
        submit_here.pack_forget()

        signed_as_user_name_shown_on_screen['text'] = 'Invalid Email or Password ! '
        signed_as_user_name_shown_on_screen['fg'] = 'red'
        status_bar['text'] = "Try Again.."
        status_bar['bg'] = "#70030a"

        back_to_previous_menu.pack()
    
    elif auth_method == "NEW-AC-ERROR" : #---------screen-if-new-account-credencials-not-cool
        inner_notification_bar.pack(side="bottom",fill="x")
        inner_notification_bar['text'] = notification_text
        app_screens('SIGNUP')
        inner_notification_bar.after(5000,inner_notification_bar.destroy)

    elif auth_method == "FEEDBACK" : #----------feebback-screen
        password.pack_forget()
        user_name.pack_forget()
        signup.pack_forget()
        I_dont_have_account.pack_forget()
        login.pack_forget()
        logout_button.pack_forget()
        signed_as_user_name_shown_on_screen.pack_forget()
        back_to_previous_menu.pack_forget()
        email.pack()
               
        if existed_account_schema:
            email.delete(0,"end")
            email.insert(0, f"{existed_account_schema['email']}")

        email.pack()
        feedback_message.pack()
        submit_here.pack()
        back_to_previous_menu.pack()


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