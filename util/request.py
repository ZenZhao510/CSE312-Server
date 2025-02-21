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
            i:int = 1
            while i < num_headers:
                header = not_body[i].split(':',1)
                self.headers[header[0]] = header[1].strip()
                # print(lines[i])
                i+=1
            # for header in self.headers:
                # print("Header: "+header+"; Value: "+self.headers[header])
            # Multiple values separated by semicolons
            # All under 'Cookie' header
            self.cookies = {}
            if "Cookie" in self.headers:
                cookieslist = self.headers["Cookies"].split(';')
                for cookie in cookieslist:
                    cookeyval = cookie.split('=')
                    self.cookies[cookeyval[0]] = cookeyval[1].strip()


def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct


if __name__ == '__main__':
    test1()
