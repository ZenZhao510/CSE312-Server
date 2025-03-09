from util.request import Request


def extract_credentials(request):
    url = request.path;

    # should only need to split once
    # separate query string from rest of path
    query = url.split("?",1)[1];
    # separate query parameters from rest of query
    query_list = query.split("&", 1);

    # should only need to splt once
    # separate parameter names from values
    user = query_list.split("=",1)[1];
    pwd = query_list.split("=",1)[1];

    credentials = [user, pwd];
    return credentials;

def validate_password(str):
    pass

