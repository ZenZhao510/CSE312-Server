import socketserver
from util.request import Request
from util.router import Router
from util.hello_path import hello_path
from util.hello_path import public_path
from util.hello_path import index_path
from util.hello_path import chat_path
from util.hello_path import post_chat

class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        self.router.add_route("GET", "/hello", hello_path, True)
        self.router.add_route("GET", "/public", public_path)
        self.router.add_route("GET", "/", index_path, True)
        self.router.add_route("GET", "/chat", chat_path, True)
        self.router.add_route("POST", "/api/chats", post_chat, True)
        # TODO: Add your routes here
        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    port = 8090
    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
