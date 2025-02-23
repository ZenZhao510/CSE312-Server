class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        
        # split by crlf crlf to separate body bytes (not to be decoded)
        data = request.split(b'\r\n\r\n')
        # if body exists, set it
        self.body = b''
        if len(data) > 1:
            self.body = data[1]
        if len(data) > 0:
            # decode method_path_http and headers
            not_body = data[0].decode().split('\r\n')
            num_headers = len(not_body) - 1
            # for line in lines:
                # print("Line: " + line)
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

if __name__ == '__main__':
    test1()
    test2()
    test3()
