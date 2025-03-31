from util.response import Response
import os
import json
import uuid
import bcrypt
import hashlib
import util.database
from util.auth import extract_credentials, validate_password
from util.multipart import parse_multipart, Multipart, MultipartPart

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
    if "auth_token" in request.cookies:
        auth_chat(request, handler)
    else:
        guest_chat(request, handler)

def guest_chat(request, handler):
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
        # print("Guest already has cookie: "+request.cookies["session"])
        message["author"] = request.cookies["session"]
    else:
        session = str(uuid.uuid4())
        # print("Guest generated new cookie: "+session)
        message["author"] = session
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        # i for some reason generated another session cookie which meant everything after has something different FUUUUUUUUUUUUCK
        session = session + "; Path=/"
        res.cookies({"session":session})
    message["id"] = str(uuid.uuid4())
    message["content"] = body["content"]
    # set updated to False
    message["updated"] = False
    # print(message)
    util.database.chat_collection.insert_one(message)

    res.text("message sent")
    # in retrospect this probably led to the doubled up cookies
    # res.cookies(request.cookies)
    # print(res.to_data())
    send = res.to_data()
    print(send)
    handler.request.sendall(send)

def auth_chat(request, handler):
    body = json.loads(request.body.decode())
    body["content"].replace("&","&amp;")
    body["content"].replace("<","&lt;")
    body["content"].replace(">","&gt;")

    res = Response()
    message = {}
    message["content"] = body["content"]

    hashed_auth = hashlib.sha256(request.cookies["auth_token"].encode()).hexdigest()
    # this accounts for auth_token removed on logout or if somehow there's an auth_token but no user in db with that token
    # somewhere in here or logout the auth_token breaks, because 
    if util.database.user_collection.find_one({"auth-token":hashed_auth}) != None:
        message["author"] = util.database.user_collection.find_one({"auth-token":hashed_auth})["username"]
    
    # do we also need to set a session token? probably not? this might actually be why logout breaks but autolab doesn't detect it
    
    # prepare message for insertion into DB
    message["id"] = str(uuid.uuid4())
    message["content"] = body["content"]
    # set updated to False
    message["updated"] = False
    util.database.chat_collection.insert_one(message)

    res.text("message sent")
    send = res.to_data()
    # print(send)
    handler.request.sendall(send)

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
    # print(res.to_data())
    handler.request.sendall(res.to_data())

def patch_chat(request, handler):
    res = Response()
    body = json.loads(request.body.decode())
    body["content"].replace("&","&amp;")
    body["content"].replace("<","&lt;")
    body["content"].replace(">","&gt;")
    id = request.path.split("/api/chats/")[1]
    # if auth_token exists (i.e. user logged in)
    if "auth_token" in request.cookies:
        if util.database.chat_collection.find_one({"id":id})["author"] != util.database.user_collection.find_one({"auth-token":hashlib.sha256(request.cookies["auth_token"].encode()).hexdigest()})["username"]:
            res.set_status("403","Forbidden")
            res.text("User lacks permission to update this message. (User)")
        else:
            util.database.chat_collection.update_one({"id":id},{"$set":{"content":body["content"],"updated":True}})
            res.text("Message updated.")
    else:
        # otherwise base off session?
        # currently as session cookies are not cleared, the logged out user would still be able to communicate as the logged in user apparently
        # weird
        if "session" not in request.cookies or util.database.chat_collection.find_one({"id":id})["author"] != request.cookies["session"]:
            res.set_status("403","Forbidden")
            res.text("User lacks permission to update this message. (Guest)")
        else:
            util.database.chat_collection.update_one({"id":id},{"$set":{"content":body["content"],"updated":True}})
            res.text("Message updated.")
    handler.request.sendall(res.to_data())

def delete_chat(request, handler):
    res = Response()
    id = request.path.split("/api/chats/")[1]
    if "auth_token" in request.cookies:
        if util.database.chat_collection.find_one({"id":id})["author"] != util.database.user_collection.find_one({"auth-token":hashlib.sha256(request.cookies["auth_token"].encode()).hexdigest()})["username"]:
            res.set_status("403","Forbidden")
            res.text("User lacks permission to delete this message. (User)")
        else:
            util.database.chat_collection.delete_one({"id":id})
        res.text("Message deleted.")
    else:
        if "session" not in request.cookies or util.database.chat_collection.find_one({"id":id})["author"] != request.cookies["session"]:
            res.set_status("403","Forbidden")
            res.text("User lacks permission to delete this message. (Guest)")
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
        # print(util.database.user_collection.find_one({"username":credentials[0]}))
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

        # compare password salt hash
        if (bcrypt.hashpw(credentials[1].encode(), salt) != util.database.user_collection.find_one({"username":credentials[0]})["password"]):
            res.set_status("400","Invalid Login")
            res.text("Incorrect Username or Password")
            handler.request.sendall(res.to_data())
    res.json(credentials)
    # read if session cookie exists
    cookies = request.cookies
    if "session" in cookies:
        # update all messages with that cookie as author retroactively
        util.database.chat_collection.update_many({"author":cookies["session"]},{"$set":{"author":credentials[0]}})
    # set auth_token with HttpOnly directive that expires in an hour
    auth_token = str(uuid.uuid4())
    res.cookies({"auth_token":auth_token+"; HttpOnly; Max-Age=3600; Path=/"})
    # print(util.database.user_collection.find_one({"username":credentials[0]}))
    # store auth_token hashed in db without a salt
    util.database.user_collection.update_one({"username":credentials[0]},{"$set":{"auth-token":hashlib.sha256(auth_token.encode()).hexdigest()}})
    
    send = res.to_data()
    handler.request.sendall(send)

def logout(request, handler):
    res = Response()
    # how are we supposed to find the user if there's no cookies in GET logout with the auth token or session cookies or anything
    # nvm i am a dumbass
    # or do we not even have to update the database
    # auth_token = request.cookies["auth_token"]
    # overwrite old auth_token with dummy token of Max-Age 0
    new_token = '0'
    if "auth_token" in request.cookies:
        hash_auth = hashlib.sha256(request.cookies["auth_token"].encode()).hexdigest()
        new_hash = hashlib.sha256(new_token.encode()).hexdigest()
        # print(util.database.user_collection.find_one({"auth-token":hash_auth}))
        util.database.chat_collection.update_one({"auth-token":hash_auth},{"$set":{"auth-token":new_hash}})
        # print(util.database.user_collection.find_one({"auth-token":new_hash})) 
        # print("old auth invalidated")
        res.text("old auth invalidated")
    res.cookies({"auth_token":request.cookies["auth_token"]+"; HttpOnly; Max-Age=0; Path=/"})
    # res.set_status("302", "Found")
    # res.headers({"Location":"Something idk"})
    send = res.to_data()
    # print(send)
    handler.request.sendall(send)

def atme(request, handler):
    res = Response()
    if "auth_token" not in request.cookies:
        res.set_status("401", "No Auth Token")
        res.json({})
    else:
        auth_token = request.cookies["auth_token"]
        ret = {}
        # print(util.database.user_collection.find_one({"auth-token":hashlib.sha256(auth_token.encode()).hexdigest()})) 
        ret["username"] = util.database.user_collection.find_one({"auth-token":hashlib.sha256(auth_token.encode()).hexdigest()})["username"]
        ret["id"] = util.database.user_collection.find_one({"auth-token":hashlib.sha256(request.cookies["auth_token"].encode()).hexdigest()})["uid"]
        res.json(ret)
    handler.request.sendall(res.to_data())

def search(request, handler):
    res = Response()

    # parse query
    search_term = request.path.split('=',1)[1]
    ret = {"users":[]}
    if search_term != "":
        # get all users
        users = list(util.database.user_collection.find())
        for user in users:
            if search_term in user["username"]:
                ret["users"].append({"id":user["uid"], "username":user["username"]})
    res.json(ret)
    handler.request.sendall(res.to_data())

def update(request, handler):
    res = Response()
    credentials = extract_credentials(request)
    auth_token = request.cookies["auth_token"]
    hashed_auth = hashlib.sha256(auth_token.encode()).hexdigest()
    username = credentials[0]
    password = credentials[1]


    if password == "":
        # only change username
        # print("Password Blank")
        util.database.user_collection.update_one({"auth-token":hashed_auth},{"$set":{"username":username}})
        res.set_status("200", "Updated OK")
    else:
        if validate_password(password) != True:
            # print("Password Invalid")
            res.set_status("400", "Password Invalid")
        else:

            util.database.user_collection.update_one({"auth-token":hashed_auth},{"$set":{"username":username}})
            salt = util.database.user_collection.find_one({"auth-token":hashed_auth})["salt"]
            new_hash = bcrypt.hashpw(password.encode(),salt)
            # print(new_hash)
            util.database.user_collection.update_one({"auth-token":hashed_auth},{"$set":{"password":new_hash}})
            res.set_status("200", "Username and Password Updated")
            # print(util.database.user_collection.find_one({"auth-token":hashed_auth}))
    handler.request.sendall(res.to_data())

def change_avatar(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/change-avatar.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def videotube(request, handler):
    res = Response()
    layout = ""
    replace = ""
    with open("public/layout/layout.html", 'r', encoding = 'utf-8') as file:
        layout = file.read()
    with open ("public/videotube.html", 'r', encoding = 'utf-8') as file:
        replace = file.read()
    res.text(layout.replace("{{content}}", replace))
    res.headers({"Content-Type":"text/html"})
    handler.request.sendall(res.to_data())

def avatar(request, handler):
    res = Response()
    multipart = parse_multipart(request)

    # grab Content-Type
    for part in multipart.parts:
        headers = part.headers
        if "Content-Type" in headers:
            ext = ""
            # grab MIME type based on ending of Content-Type
            if headers["Content-Type"] == "image/jpeg":
                ext = "jpg"
            else:
                ext = headers["Content-Type"].split("/")[1]
            
            filepath = "public/img/profile-pics/" + str(uuid.uuid4()) + "." + ext
            # upload to public/img/profile-pics/{uuid}.{ext}
            with open(filepath, 'wb') as file:
                file.write(part.content)
            
            # update user's messages to include imageURL field
            # take auth_token, find the user it's associated with
            # after that, update all of that's user's messages
            if "auth_token" in request.cookies:
                author = util.database.user_collection.find_one({"auth-token":hashlib.sha256(request.cookies["auth_token"].encode()).hexdigest()})["username"]
                util.database.chat_collection.update_many({"author":author},{"$set":{"imageURL":filepath}})

    res.text("Avatar Updated")
    handler.request.sendall(res.to_data())
    # print(multipart.boundary)
    # print(multipart.parts)

def videotube_upload(request, handler):
    pass

def videotube_view(request, handler):
    pass

# if __name__ == '__main__':
    # database.chat_collection.drop()
    # database.user_collection.drop()