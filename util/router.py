from util.response import Response

class Router:

    def __init__(self):
        routes = []
        pass

    def add_route(self, method, path, action, exact_path=False):
        new_route = Route()
        new_route.set_method(self,method).set_path(self,path).set_action(self,action).set_exact_path(self,exact_path)
        self.routes.add(new_route)
        pass

    def route_request(self, request, handler):
        # check if any route is a substring? potential problem if routes exist to "/public" and "/public/img"
        for route in self.routes:
            if (request.path.startswith(route.path)) and (request.method == route.method):
                if (route.exact_path == True) and (route.path != request.path):
                    pass
                else:
                    # test if path exists? "/public/img" is a substring of "public/img/dog.jpg" 
                    # #but what if "dog.jpg" doesn't exist in "public/img"
                    return
        not_found = Response()
        not_found.set_status(not_found,"404","Not Found").text(not_found,"The requested resource cannot be found")
        handler.request.sendall(not_found.to_data())
        pass

class Route:
    def __init__(self):
        self.method;
        self.path;
        self.action;
        self.exact_path = False;

    def set_method(self, method):
        self.method = method
        return self

    def set_path(self, path):
        self.path = path
        return self

    def set_action(self, action):
        self.action = action
        return self

    def set_exact_path(self, exact_path):
        self.exact_path = exact_path
        return self