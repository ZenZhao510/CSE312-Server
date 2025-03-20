from request import Request

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

    pass