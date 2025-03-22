#DB Functions



from pymongo import MongoClient
from cryptography.fernet import Fernet
from  flask_bcrypt import Bcrypt

import bcrypt

#Create pymongo client
client = MongoClient("mongodb://localhost:27017/")
db = client["JIRA"]
user_collection = db["userdetails"]
jira_collection = db["jiradetails"]


#key = Fernet.generate_key()
key = b'MBCqkKHCr9xk06kvW2M_Uz1qGwe7NiArUYhiJFCsSkE='
cipher_suite = Fernet(key)


def encrypt_token(message):
    return cipher_suite.encrypt(message.encode())

def decrypt_token(encrypted_message):
    print("Encrypted message", encrypted_message)
    return cipher_suite.decrypt(encrypted_message).decode()

def get_user_details(email):
    return user_collection.find_one({"email" : email})


def insert_user_details(name, email, password):
    #hashed_password = bcrypt.generate_password_hash(password)
    print("inside insert_user_details :",name, email, password)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one({"name": name, "email" : email, "password":hashed_password})
    
def update_user_details(name, email, password):
    #hashed_password = bcrypt.generate_password_hash(password)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_collection.update_one({"email":email}, {"$set":{"name" : name, "password" : hashed_password}})

def update_jira_details(details):
    details["token"] = encrypt_token(details["token"])
    jira_collection.update_one(
        {"uid" : details["uid"], "type":details["type"]},
        {"$set" : details},
        upsert=True
    )

def get_jira_details(email, version="JIRA Cloud"):
    print("inside get_jira_details:",email, version)
    details = jira_collection.find_one({"email" : email, "type" : version})
    print("get_jira_details :", details)
    if details:
        details["token"] = decrypt_token(details["token"])
    print("Jira details retrived from db",details)
    return details

#list of all db functions


'''
input      : email,URL,userName,token
collection : JIRA_Details 
output : {
           email : "",
           URL : "",
           userName : "",
           token : ""}


def update_JIRA_Details(email,URL,userName,token):
    return True





input      : Login user email id [session]
collection : JIRA_Details 
output : {
           URL : "",
           userName : "",
           token : ""}

'''
