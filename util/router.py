class Router:

    def __init__(self):
        routes = {}
        pass

    def add_route(self, method, path, action, exact_path=False):
        method_path = method + " " + path
        self.routes[method_path] = {"action":action,"exact_path":exact_path}
        pass

    def route_request(self, request, handler):
        method_path = request.method + " " + request.path
        if  (method_path in self.routes):
            pass
        else:
            # call route for 404
            not_found = Response()
        pass
