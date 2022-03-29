import os


def save_logs_on_system(login_data):
    
    os.chdir(f"{os.getcwd()}")

    with open("user_login.file","w") as f:
        f.write(str(login_data))







