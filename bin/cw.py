from time import sleep
import pyperclip as pc
import pymongo


DBClient = pymongo.MongoClient("mongodb://localhost:27017")
DB = DBClient['copyword']
userbase = DB['userbase']

copied_object = pc.paste()

def add_word_on_server():
    copied_object = pc.paste()
    copy_model = {'copy_object':copied_object}
    userbase.insert_one({"_id":1,"copy_object":copy_model})

def update_word_on_sever():
    update_this = userbase.find_one({"_id":"1"})
    # update_this = update_this["copy_object"]
    with_new_copied_object = {"$set" :{"copy_object": f"{pc.paste()}"}}

    userbase.update_one(update_this , with_new_copied_object)




def main_run():
    add_word_on_server()
    while True:
        update_word_on_sever()
        sleep(4)




if __name__ == "__main__":
    main_run()
