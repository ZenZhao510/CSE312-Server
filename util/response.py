import json


class Response:
    def __init__(self):
        self.status_code = "200"
        self.status_msg = "OK"
        self.headers_dict = {}
        self.cookies_dict = {}
        self.body = b""
        pass

    def set_status(self, code, text):
        self.status_code = code
        self.status_msg = text
        return self
        pass

    def headers(self, headers):
        for header in headers:
            # do we update headers that already exist in headers_dict
            # if input dict has same keys but different vals as headers_dict
            #
            # we probably should...
            #
            # if header.key in self.headers_dict:
            # an if statement is probably not needed, the below code should work for both new and existing headers
            # this does not work for duplicate headers, but we wouldn't be using a dict for those anyways
            self.headers_dict[header] = str(headers[header])
        return self
        pass

    # do i have to? depending on how i parse headers i probably shouldn't have to add extra here
    # actually, since this can be called multiple times, i guess it should still update the headers dictionary?
    # ... but as Set-Cookie can be included as a header multiple times, probably not
    # it's only to_data() that probably doesn't have to look at both headers and cookies separately
    def cookies(self, cookies):
        # add cookies to cookies dict
        for cookie in cookies:
            self.cookies_dict[cookie] = str(cookies[cookie])
        return self
        pass

    def bytes(self, data):
        # json should not be in here if bytes is
        # just a safeguard against calling bytes or text after json
        if "Content-Type" in self.headers_dict and self.headers_dict["Content-Type"] == "application/json":
            self.headers_dict.pop("Content-Type")
            self.body = b""
        self.body = self.body + data
        return self
        pass

    def text(self, data):
        self.bytes(data.encode())
        return self
        pass

    def json(self, data):
        self.headers({"Content-Type":"application/json"})
        self.body = json.dumps(data, default=str).encode()
        return self
        pass

    def to_data(self):
        if ("Content-Type" not in self.headers_dict):
            self.headers({"Content-Type":"text/plain; charset=utf-8"})
        self.headers({"X-Content-Type-Options":"nosniff", "Content-Length":str(len(self.body))})
        ret = "HTTP/1.1 " + str(self.status_code) + " " + str(self.status_msg) + "\r\n"
        for header in self.headers_dict:
            ret = ret + str(header) + ": " + str(self.headers_dict[header]) + "\r\n"
        for cookie in self.cookies_dict:
            ret = ret + "Set-Cookie: " + str(cookie) + "=" + str(self.cookies_dict[cookie]) + "\r\n"
        ret = ret + "\r\n"
        return ret.encode() + self.body


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()
    # print(expected)
    # print(actual)
    assert expected == actual

def test2():
    res = Response()
    res.text("hi")
    res.json({"id":1})
    # json overwrites text/bytes 
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 9\r\n\r\n{"id": 1}'
    actual = res.to_data()
    # print(expected)
    # print(actual)
    assert expected == actual

def test3():
    res = Response()
    res.json({"id":1})
    res.bytes(b"55")
    res.text("apples")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 8\r\n\r\n55apples'
    actual = res.to_data()
    # print(expected)
    # print(actual)
    assert expected == actual

def test4():
    res = Response()
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 0\r\n\r\n'
    actual = res.to_data()
    assert expected == actual

def test5():
    res = Response()
    res.set_status("404", "Not Found")
    res.text("Requested resource cannot be found")
    expected = b'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 34\r\n\r\nRequested resource cannot be found'
    actual = res.to_data()
    # print(expected)
    # print(actual)
    assert expected == actual


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()

