from time import sleep
from tkinter import Button, Label, Tk, Entry
import ast
import os

os.chdir(f"{os.getcwd()}\\copyword\\bin")
existed_account_schema = ""

root = Tk()
root.geometry("350x200")
root.title("CopyWord")

main_header_title = Label(root,text="CopyWord PC Client",font="sans 14").pack()
# --------------------------------------------------------------------------------------
email_form = Entry(root)
def connection_status():
    
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
        email = login_values_in_dictionary['email']
        
        status_bar['text'] = "Login Succees"
    except:
        email_form.pack()
        status_bar['text'] = "You're logged out !!!"

status_bar = Label(text="Anas-Dew", bg="Black", fg="White", font="sans 9")
status_bar.pack(side="bottom",anchor="w")

# Login = Button(root, text="Login",command=main_header_title).pack()
if __name__ == "__main__":

    connection_status()
    root.mainloop()