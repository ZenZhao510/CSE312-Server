class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        
        # split by crlf crlf to separate body bytes (not to be decoded)
        data = request.split(b'\r\n\r\n',1)
        # if body exists, set it
        self.body = b''
        if len(data) > 1:
            self.body = data[1]
        if len(data) > 0:
            # decode method_path_http and headers
            not_body = data[0].decode().split('\r\n')
            # print(not_body)
            num_headers = len(not_body) - 1
            # for line in lines:
                # print("Line: " + line)
            if len(not_body) > 1:
                method_path_http = not_body[0].split()
                # print("Request: " + data)
                # have to figure out how to parse bytes
                # GET POST etc
                # print(method_path_http)
                self.method = method_path_http[0]
                # Path Requested
                self.path = method_path_http[1]
                # HTTP ver
                self.http_version = method_path_http[2]
                # Host
                self.headers = {}
                i:int = 0
                while i < num_headers:
                    header = not_body[i+1].split(':',1)
                    self.headers[header[0].strip()] = header[1].strip()
                    # print(lines[i])
                    i+=1
                # for header in self.headers:
                    # print("Header: "+header+"; Value: "+self.headers[header])
                # Multiple values separated by semicolons
                # All under 'Cookie' header
                self.cookies = {}
                if "Cookie" in self.headers:
                    cookieslist = self.headers["Cookie"].split(';')
                    for cookie in cookieslist:
                        # print(cookie)
                        cookeyval = cookie.split('=')
                        # print(cookeyval)
                        self.cookies[cookeyval[0].strip()] = cookeyval[1].strip()


def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert request.path == "/"
    assert request.http_version == "HTTP/1.1"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert "Connection" in request.headers
    assert request.headers["Connection"] == "keep-alive" # multiple headers can be inserted
    assert bool(request.cookies) == False # no cookies should exist
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

def test2():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: id=1; pig = False\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert "Cookie" in request.headers
    assert request.headers["Cookie"] == "id=1; pig = False"
    assert bool(request.cookies) == True
    assert "id" in request.cookies
    assert request.cookies["id"] == "1"
    assert "pig" in request.cookies
    assert request.cookies["pig"] == "False"
    assert request.body == b""  

def test3():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: id=1\r\n\r\n')
    assert "Cookie" in request.headers
    assert request.headers["Cookie"] == "id=1"
    assert bool(request.cookies) == True
    assert "id" in request.cookies
    assert request.cookies["id"] == "1"

def test4():
    request = Request(b'GET /public/imgs/favicon.ico HTTP/1.1\r\nHost: localhost:8090\r\nConnection: keep-alive\r\nsec-ch-ua-platform: "Windows"\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\r\nsec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"\r\nsec-ch-ua-mobile: ?0\r\nAccept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: no-cors\r\nSec-Fetch-Dest: image\r\nReferer: http://localhost:8090/\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9,ja;q=0.8\r\nCookie: auth_token=2800a8e6-8a9b-4f21-8b40-ebfd8f960c1c\r\n\r\n')
    assert "Cookie" in request.headers
    assert request.headers["Cookie"] == 'auth_token=2800a8e6-8a9b-4f21-8b40-ebfd8f960c1c'
    assert bool(request.cookies) == True
    assert 'auth_token' in request.cookies
    assert request.cookies['auth_token'] == '2800a8e6-8a9b-4f21-8b40-ebfd8f960c1c'

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
