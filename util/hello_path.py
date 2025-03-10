from util.response import Response
import os
import json
import uuid
import bcrypt
import hashlib
import util.database
from util.auth import extract_credentials, validate_password

# This path is provided as an example of how to use the router
def hello_path(request, handler):
    res = Response()
    res.text("hello")
    handler.request.sendall(res.to_data())

def public_path(request, handler):
    res = Response()
    img = ["jpg","ico","webp","gif"]
    txt = ["js","css"]
    # can't have '/' in filepath according to @92
    filepath = request.path[1:]
    path_array = filepath.split('.')
    ext = path_array[1]
    # check if filepath exists before opening
    # Tina confirmed os is allowed for this
    if os.path.exists(filepath):
        with open(filepath, 'rb') as file:
            read_data = file.read()
            # use file extensions to get MIME type
            if ext in img:
                res.bytes(read_data)
                if ext == "ico":
                    res.headers({"Content-Type":"image/x-icon"})
                elif ext == "jpg":
                    res.headers({"Content-Type":"image/jpeg"})
                else:
                    res.headers({"Content-Type":"image/"+ext})
            elif ext in txt:
                res.bytes(read_data)
                if ext == "js":
                    res.headers({"Content-Type":"text/javascript"})
                else:
                    res.headers({"Content-Type":"text/"+ext})        
        handler.request.sendall(res.to_data())
    else:
        res.set_statusset_status("404","Not Found").text("The requested resource cannot be found")
        handler.request.sendall(res.to_data())


def index_path(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/index.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def chat_path(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/chat.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def register_path(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/register.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def login_path(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/login.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def settings_path(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/settings.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def search_users_path(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/search-users.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def post_chat(request, handler):
    # parse incoming request json
    body = json.loads(request.body.decode())
    body["content"].replace("&","&amp;")
    body["content"].replace("<","&lt;")
    body["content"].replace(">","&gt;")
    # prepare response for a valid message
    res = Response()
    message = {}
    message["content"] = body["content"]
    if "session" in request.cookies:
        message["author"] = request.cookies["session"]
        # session cookie should be set later by the cookies method
    else:
        session = str(uuid.uuid4()) + "; Path=/"
        message["author"] = session
        res.cookies({"session":session})
    # should there be a separate "id" asides from "_id"?
    message["id"] = str(uuid.uuid4())
    message["content"] = body["content"]
    # set updated to False
    message["updated"] = False
    # print(message)
    util.database.chat_collection.insert_one(message)
    
    res.text("message sent")
    res.cookies(request.cookies)
    # print(res.to_data())
    handler.request.sendall(res.to_data())

def get_chat(request, handler):
    res = Response()
    # grab every chat and simply stuff them into a list
    chats = list(util.database.chat_collection.find({}))
    # print(chats)
    for chat in chats:
        chat["content"] = chat["content"].replace("&","&amp;")
        chat["content"] = chat["content"].replace("<","&lt;")
        chat["content"] = chat["content"].replace(">","&gt;")
    res.json({"messages":chats})
    print(res.to_data())
    handler.request.sendall(res.to_data())

def patch_chat(request, handler):
    res = Response()
    body = json.loads(request.body.decode())
    body["content"].replace("&","&amp;")
    body["content"].replace("<","&lt;")
    body["content"].replace(">","&gt;")
    id = request.path.split("/api/chats/")[1]
    if "session" not in request.cookies or util.database.chat_collection.find_one({"id":id})["author"] != request.cookies["session"]:
        res.set_status("403","Forbidden")
        res.text("User lacks permission to update this message.")
    else:
        util.database.chat_collection.update_one({"id":id},{"$set":{"content":body["content"],"updated":True}})
        res.text("Message updated.")
    handler.request.sendall(res.to_data())

def delete_chat(request, handler):
    res = Response()
    id = request.path.split("/api/chats/")[1]
    if "session" not in request.cookies or util.database.chat_collection.find_one({"id":id})["author"] != request.cookies["session"]:
        res.set_status("403","Forbidden")
        res.text("User lacks permission to delete this message.")
    else:
        util.database.chat_collection.delete_one({"id":id})
        res.text("Message deleted.")
    handler.request.sendall(res.to_data())

def register(request, handler):
    res = Response()
    credentials = extract_credentials(request)
    valid_pwd = validate_password(credentials[1])
    if (not valid_pwd):
        res.set_status("400","Invalid Registration")
        res.text("Password needs to be at least 8 characters long, have at least one lowercase character, have at least one uppercase character, and a special character")
        handler.request.sendall(res.to_data())
    # if user exists
    if (util.database.user_collection.find_one({"username":credentials[0]}) != None):
        res.set_status("400","Invalid Registration")
        res.text("Username already exists")
        handler.request.sendall(res.to_data())
    else:
        salt = bcrypt.gensalt()
        user = {"uid":str(uuid.uuid4()), "username":credentials[0], "password":bcrypt.hashpw(credentials[1].encode(), salt), "salt":salt}
        util.database.user_collection.insert_one(user)
    res.json(credentials)

    handler.request.sendall(res.to_data())

def login(request, handler):
    res = Response()
    credentials = extract_credentials(request)
    # see if user exists
    user_exists = False;
    if (util.database.user_collection.find_one({"username":credentials[0]}) != None):
        user_exists = True;
    if (not user_exists):
        # make sure to have this status message be the same for pw and user at submission (no hints for attackers)
        res.set_status("400","Invalid Login")
        res.text("Incorrect Username or Password")
        handler.request.sendall(res.to_data())
    else:
        salt = util.database.user_collection.find_one({"username":credentials[0]})["salt"]

        # compare password salt has
        if (bcrypt.hashpw(credentials[1].encode(), salt) != util.database.user_collection.find_one({"username":credentials[0]})["password"]):
            res.set_status("400","Invalid Login")
            res.text("Incorrect Username or Password")
            handler.request.sendall(res.to_data())
    res.json(credentials)

    # set auth_token with HttpOnly directive that expires in an hour
    auth_token = str(uuid.uuid4())
    res.headers({"auth_token":auth_token+"; HttpOnly; Max-Age=3600"})
    # store auth_token hashed in db without a salt
    util.database.chat_collection.update_one({"username":credentials[0]},{"$set":{"auth-token":hashlib.sha256(auth_token.encode()).hexdigest()}})
    handler.request.sendall(res.to_data())

def logout(request, handler):
    res = Response()
    # how are we supposed to find the user if there's no cookies in GET logout with the auth token or session cookies or anything
    # or do we not even have to update the database
    # auth_token = request.cookies["auth_token"]
    # overwrite old auth_token with dummy token of Max-Age 0
    new_token = str(uuid.uuid4())
    # util.database.chat_collection.update_one({"auth_token":auth_token},{"$set":{"auth-token":hashlib.sha256(new_token.encode()).hexdigest()}})
    res.headers({"auth_token":new_token+"; HttpOnly; Max-Age=0"})
    res.set_status("302", "Found")
    res.headers({"Location":"Something idk"})
    handler.request.sendall(res.to_data())