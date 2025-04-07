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
from util.paths import videotube_upload
from util.paths import videotube_view
from util.paths import test_websocket
from util.paths import drawing_board
from util.paths import direct_messaging
from util.paths import video_call
from util.paths import video_call_room

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

from util.paths import avatar
from util.paths import upload
from util.paths import retrieve
from util.paths import retrieve_one

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
        self.router.add_route("GET", "/videotube/upload", videotube_upload, True)
        self.router.add_route("GET", "/videotube/videos/", videotube_view)
        self.router.add_route("GET", "/test-websocket", test_websocket, True)
        self.router.add_route("GET", "/drawing-board", drawing_board, True)
        self.router.add_route("GET", "/direct-messaging", direct_messaging, True)
        self.router.add_route("GET", "/video-call", video_call, True)
        self.router.add_route("GET", "/video-call/", video_call_room)

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

        # avatar upload route
        self.router.add_route("POST", "/api/users/avatar", avatar, True)
        # video upload route
        self.router.add_route("POST", "/api/videos", upload, True)
        # video view route
        self.router.add_route("GET", "/api/videos", retrieve, True)
        self.router.add_route("GET", "/api/videos/", retrieve_one)
        # TODO: Add your routes here
        super().__init__(request, client_address, server)

    def handle(self):
        content_length = None
        buffer = b""
        headers = b""
        # print(buffer)
        # print("--- cleared buffer ---\n\n")

        while True:
            # this only gets 2048 bytes of data, requires buffering for large requests involving files
            received_data = self.request.recv(2048)
            # print(self.client_address)
            # print("--- received data ---")
            # print(received_data)
            # print("--- end of data ---\n\n")
            # if no more bytes are sent, break
            if not received_data:
                break

            buffer += received_data
            # print(buffer)
            # print("--- updated buffer ---\n\n")

            if content_length is None:
                headers, body = buffer.split(b"\r\n\r\n", 1)
                buffer = body
                headers_list = headers.split(b"\r\n")[1:]
                headers_dict = {}
                for header in headers_list:
                    headers_dict[header.split(b":",1)[0].strip()] = header.split(b":",1)[1].strip()
                if b"Content-Length" in headers_dict:
                    content_length = int(headers_dict[b"Content-Length"])
                else:
                    content_length = 0
            
            if content_length is not None and len(buffer) >= content_length:
                request = Request(headers + b"\r\n\r\n" + buffer[:content_length])
                # print(request.cookies)
                # print("--- received full data ---")
                # print(headers)
                # print(buffer)
                # print("--- end of full data ---\n\n")
                buffer = buffer[content_length:]
                # print(buffer)
                # print("--- remainder of buffer of full data ---\n\n")
                content_length = None
                self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    # make sure to change back to 8080 for submissions
    port = 8090
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
