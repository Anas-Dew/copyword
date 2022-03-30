from time import sleep
from tkinter import Button, Label, Tk, Entry
import ast
import os

os.chdir(f"{os.getcwd()}\\copyword\\bin")
existed_account_schema = ""

root = Tk()

root.geometry("350x200")
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
        # login_or_signup_screen("LOGIN")
        
        


def login_or_signup_screen(auth_method:str):
    global existed_account_schema
    
    email = Entry(root, width=30, bg="#383838", fg="White")
    name = Entry(root, width=30, bg="#383838", fg="White")
    password = Entry(root, width=30, bg="#383838", fg="White")

    signed_as = Label(root,text=f"Welcome, Anas",bg="#1e1e21",fg="White",font="sans 14")
    logout = Button(root, text="Logout", width=25, height=1,command=lambda: login_or_signup_screen("LOGIN"), activeforeground="white", activebackground="#383838")
    
    I_dont_have_account = Button(root, text="I don't have account", width=25, height=1,command=lambda: login_or_signup_screen("SIGNUP"), activeforeground="white", activebackground="#383838")
    
    login = Button(root, text="Login", width=25, height=1,command=None, activeforeground="white", activebackground="#383838")
        

    if auth_method == "LOGIN" :


        # email.pack(pady=3)
        # password.pack(pady=3)
        
        # login.pack(padx=2, pady=7)
                
        I_dont_have_account.pack(pady=0)

        logout.pack_forget()
        signed_as.pack_forget()


    elif auth_method == "SIGNUP" :
        email.pack_forget()
        password.pack_forget()
        Login.pack_forget()
        I_dont_have_account.pack_forget()

        name = Entry(root, width=30, bg="#383838", fg="White")
        name.pack(pady=3)
        
        email = Entry(root, width=30, bg="#383838", fg="White")
        email.pack(pady=3)

        password = Entry(root, width=30, bg="#383838", fg="White")
        password.pack(pady=3)
        
        Login = Button(root, text="Login", width=25, height=1,command=None, activeforeground="white", activebackground="#383838").pack(padx=2, pady=14)
    
    elif auth_method == "LOGOUT" :
        
        signed_as.pack(pady=10)

        logout.pack(padx=2, pady=7)

    else:
        connection_status()


status_bar = Label(text="Anas-Dew", bg="Black", fg="White", font="sans 9")
status_bar.pack(side="bottom",fill="x")


if __name__ == "__main__":

    connection_status()
    root.mainloop()