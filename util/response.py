import json


class Response:
    def __init__(self):
        self.status_code = ""
        self.status_msg = ""
        self.headers_dict = {}
        self.cookies_dict = {}
        self.body =b""
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
            # actually we should, we have to update header value with each new cookie added
            #
            # if header.key in self.headers_dict:
            # an if statement is probably not needed, the below code should work for both new and existing headers
            # this does not work for duplicate headers, but we wouldn't be using a dict for those anyways
            self.headers_dict[header] = headers[header]
        return self
        pass

    # do i have to? depending on how i parse headers i probably shouldn't have to add extra here
    # actually, since this can be called multiple times, i guess it should still update the headers dictionary
    # it's only to_data() that probably doesn't have to look at both headers and cookies separately
    def cookies(self, cookies):
        # add cookies to cookies dict
        for cookie in cookies:
            self.cookies_dict[cookie] = cookies[cookie]
        # add new cookies to headers
        val = ""
        for cookie in self.cookies_dict:
            val = val + cookie + "=" + self.cookies_dict[cookie] + "; "
        self.headers(self, {"Cookies": val})
        return self
        pass

    def bytes(self, data):
        
        return self
        pass

    def text(self, data):

        return self
        pass

    def json(self, data):
        self.headers({"Content-Type":"application/json"})
        return self
        pass

    def to_data(self):
        return b''


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()


if __name__ == '__main__':
    test1()
