from time import sleep
from tkinter import Button, Label, Tk, Entry
import ast
import os
from typing import Optional

os.chdir(f"{os.getcwd()}\\copyword\\bin")
existed_account_schema = ""

root = Tk()

# root.geometry("350x200")
root.geometry("350x500")
root.title("CopyWord")
root.configure(background='#1e1e21')
root.resizable('False','False')

main_header_title = Label(root,text="CopyWord PC Client",bg="#1e1e21",fg="White",font="sans 14").pack(pady=10)
# --------------------------------------------------------------------------------------
def connection_status():
    global existed_account_schema
    status_bar['text'] = "Loading..."

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

        login_or_signup_screen("LOGOUT")

    except:
        status_bar['text'] = "You're logged out !!!"
        status_bar['bg'] = "#70030a"
        login_or_signup_screen("LOGIN")

# ------------------------------------------------------------------------------------------------------------------


logout_button = Button(root, text="Logout", width=25, height=1,command=lambda: login_or_signup_screen("LOGIN"), activeforeground="white", activebackground="#383838")
I_dont_have_account = Button(root, text="I don't have account", width=25, height=1,command=lambda: login_or_signup_screen("SIGNUP"), activeforeground="white", activebackground="#383838")
    
login = Button(root, text="Login", width=25, height=1,command=None, activeforeground="white", activebackground="#383838")
signup = Button(root, text="Create New Account", width=25, height=1,command=None, activeforeground="white", activebackground="#383838")
back_to_previous_menu = Button(root, text="Back", width=25, height=1, activeforeground="white", activebackground="#383838")

# ---------------------
signed_as_user_name_shown_on_screen = Label(root,text=f"Welcome, Anas",bg="#1e1e21",fg="White",font="sans 14")
# ---------------------
user_name = Entry(root, width=30, bg="#383838", fg="White")
email = Entry(root, width=30, bg="#383838", fg="White")
password = Entry(root, width=30, bg="#383838", fg="White")
# -------------------------------------------------------------------------------------------------------------------
def login_or_signup_screen(auth_method:str, name:Optional[str] = None):
    global existed_account_schema
            

    if auth_method == "LOGIN" :

        signed_as_user_name_shown_on_screen.pack_forget()
        logout_button.pack_forget()

        email.pack(pady=3)
        email.insert(0, 'Email')
        
        password.pack(pady=3)
        password.insert(0, 'Password')

        login.pack(padx=2, pady=7)

        I_dont_have_account.pack()



    elif auth_method == "SIGNUP" :
        
        # email.pack_forget()
        # password.pack_forget()
        login.pack_forget()
        I_dont_have_account.pack_forget()

        user_name.pack(pady=3)
        user_name.insert(0, 'Name')

        # email.pack(pady=3)
        # email.insert(0, 'Email')
        
        # password.pack(pady=3)
        # password.insert(0, 'Password')

        signup.pack(padx=2, pady=7)
        # back_to_previous_menu.pack()
    
    elif auth_method == "LOGOUT" :
        
        signed_as_user_name_shown_on_screen.pack(pady=10)
        logout_button.pack(padx=2, pady=7)

    else:
        connection_status()


status_bar = Label(text="Anas-Dew", bg="Black", fg="White", font="sans 9")
status_bar.pack(side="bottom",fill="x")


if __name__ == "__main__":

    connection_status()
    root.mainloop()