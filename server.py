import socketserver
from util.request import Request
from util.router import Router
from util.paths import hello_path
from util.paths import public_path
from util.paths import index_path
from util.paths import chat_path
from util.paths import register_path
from util.paths import login_path
from util.paths import settings_path
from util.paths import search_users_path
from util.paths import change_avatar
from util.paths import videotube

from util.paths import post_chat
from util.paths import get_chat
from util.paths import patch_chat
from util.paths import delete_chat

from util.paths import register
from util.paths import login
from util.paths import logout
from util.paths import atme
from util.paths import update
from util.paths import search

from util.paths import videotube_upload
from util.paths import videotube_view

class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        # static files
        self.router.add_route("GET", "/hello", hello_path, True)
        self.router.add_route("GET", "/public", public_path)
        self.router.add_route("GET", "/", index_path, True)
        self.router.add_route("GET", "/chat", chat_path, True)
        self.router.add_route("GET", "/register", register_path, True)
        self.router.add_route("GET", "/login", login_path, True)
        self.router.add_route("GET", "/settings", settings_path, True)
        self.router.add_route("GET", "/search-users", search_users_path, True)
        self.router.add_route("GET", "/change-avatar", change_avatar, True)
        self.router.add_route("GET", "/videotube", videotube, True)

        # chat routes
        self.router.add_route("POST", "/api/chats", post_chat, True)
        self.router.add_route("GET", "/api/chats", get_chat, True)
        self.router.add_route("PATCH", "/api/chats", patch_chat)
        self.router.add_route("DELETE", "/api/chats", delete_chat)

        # register routes
        self.router.add_route("POST", "/register", register, True)
        # login routes
        self.router.add_route("POST", "/login", login, True)
        # logout routes
        self.router.add_route("GET", "/logout", logout, True)
        # @me routes
        self.router.add_route("GET", "/api/users/@me", atme, True)
        # search routes
        self.router.add_route("GET", "/api/users/search", search)
        # update routes
        self.router.add_route("POST", "/api/users/settings", update, True)

        # video upload route
        self.router.add_route("POST", "/videotube/upload", videotube_upload)
        # video view route
        self.router.add_route("GET", "/videotube/videos", videotube_view)
        # TODO: Add your routes here
        super().__init__(request, client_address, server)

    def handle(self):
        # this only gets 2048 bytes of data, requires buffering for large requests involving files
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    # make sure to change back to 8080 for submissions
    port = 8080
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
