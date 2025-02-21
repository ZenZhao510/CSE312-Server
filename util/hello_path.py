from util.response import Response


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
    with open(filepath, 'r') as file:
        read_data = file.read()
        # use file extensions to get MIME type
        if ext in img:
            res.bytes(res, read_data)
            if ext == "ico":
                res.headers(res,{"Content-Type":"image/x-icon"})
            else:
                res.headers(res,{"Content-Type":"image/"+ext})
        elif ext in txt:
            res.bytes(res, read_data)
            res.headers(res,{"Content-Type":"text"/+ext})
        
    handler.request.sendall(res.to_data())


def index_path(request, handler):
    res = Response()
    handler.request.sendall(res.todata())

def chat_path(request, handler):
    res = Response()
    handler.request.sendall(res.todata())

def not_found(request, handler):
    res = Response()
    res.set_status(res, "404", "Not Found")
    res.text(res, "The requested resource cannot be found")
    handler.request.sendall(res.to_data())
