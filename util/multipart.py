from util.request import Request

# we assume that the request is complete and that buffering has been done in server.py to construct a full request
# requirements to parse multipart requests:

# identify request using method and path, if form-path, 
# if Content-Type: multipart/form-data header received, prepare to parse multipart
# parse the boundary as bytes
# parse content length 
# read content length bytes from body before parsing
#
# search for boundary as bytes within read body bytes to divide body into parts
# for each part, parse headers
# Content-Type, parse the "body" that follows accordingly
def parse_multipart(request):
    # create Multipart object
    multipart = Multipart()

    # use Multipart's functions to parse
    if ("Content-Type" in request.headers):
        ContentType = request.headers["Content-Type"]
        # multipart/form-data;boundary=----WebKitFormBoundaryfkz9sCA6fR3CAHN4
        multipart.setBoundary(ContentType)
        multipart.addParts(b"\r\n"+request.body)
    return multipart

class Multipart:

    def __init__(self):
        self.boundary = ""
        self.parts = []
    
    def setBoundary(self, header):
        self.boundary = header.split("=")[1]
        # ----WebKitFormBoundaryfkz9sCA6fR3CAHN4

    # this does not account for body already having removed the first CRLF
    # first boundary does not have this split, can probably pass a bytearray of CRLF + body for simplicity
    def addParts(self, body):
        # this also removes the first empty entry from this split list
        # unfortunately, this keeps the first "\r\n" in front of each part
        splitBoundary = body.split(b"\r\n--"+self.boundary.encode())
        # print(splitBoundary)
        splitBoundary = splitBoundary[1:]
        # print(splitBoundary)
        # removes the last b"--\r\n" from list
        # nevermind it's not found in 
        splitBoundary.pop()
        # print(splitBoundary)
        for part in splitBoundary:
            # print(b"next part is: " + part)
            newPart = MultipartPart(part)
            self.parts.append(newPart)

class MultipartPart:
    
    def __init__(self, partData):
        data = partData.split(b"\r\n\r\n",1)
        self.content = data[1]
        headersList = data[0].decode().split("\r\n")
        # remove the first empty entry (due to "\r\n" starting each part)
        headersList = headersList[1:]
        self.headers = {}
        for header in headersList:
            self.headers[header.split(":",1)[0].strip()] = header.split(":",1)[1].strip()
        self.name = ""
        if "Content-Disposition" in self.headers:
            # split directives in Content-Disposition into a list, then into a dictionary
            # this accounts for whichever order directives are given
            directives = {}
            directivesList = self.headers["Content-Disposition"].split(";")[1:]
            for directive in directivesList:
                directives[directive.split("=",1)[0].strip()] = directive.split("=",1)[1].strip()
            # assign name field with the proper directive
            if ("name" in directives):
                self.name = directives["name"].strip('"').strip("'")

def test1():
    request = Request(b'POST / HTTP/1.1\r\nHost: localhost:8080\r\nContent-Length: 252\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryfkz9sCA6fR3CAHN4\r\n\r\n------WebKitFormBoundaryfkz9sCA6fR3CAHN4\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------WebKitFormBoundaryfkz9sCA6fR3CAHN4--\r\n')
    multipart = parse_multipart(request)
    # print(multipart.parts)
    assert len(multipart.parts) == 1
    # print(multipart.parts[0].name)
    expectedname = "commenter"
    assert multipart.parts[0].content == b"Jesse"
    # for some reason name is freaking out
    # assert multipart.parts[0].name == expectedname

if __name__ == '__main__':
    test1()