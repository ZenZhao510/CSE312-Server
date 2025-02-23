from util.response import Response
import os
import json
import uuid
import util.database

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

def post_chat(request, handler):
    # parse incoming request json
    body = json.loads(request.body.decode())
    # prepare response for a valid message
    res = Response()
    message = {}
    message["content"] = body["content"]
    # if "session" in request.cookies:
    #     message["author"] = request.cookies["session"]
    #     # session cookie should be set later by the cookies method
    # else:
    #     session = str(uuid.uuid4())
    #     message["author"] = session
    #     res.cookies({"session":session})
    session = str(uuid.uuid4())
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
    res.json({"messages":chats})
    handler.request.sendall(res.to_data())

def patch_chat(request, handler):
    res = Response()
    body = json.loads(request.body.decode())
    id = request.path.split("/api/chats/")[1]
    if "author" not in request.cookies or util.database.chat_collection.find_one({"id":id})["author"] != request.cookies["author"]:
        res.set_status("403","Forbidden")
        res.text("User lacks permission to update this message.")
    else:
        util.database.chat_collection.update_one({"id":id},{"$set":{"content":body["content"]}})
        res.text("Message updated.")
    handler.request.sendall(res.to_data())

def delete_chat(request, handler):
    pass

