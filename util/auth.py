from util.request import Request
from string import ascii_lowercase
from string import ascii_uppercase
from string import ascii_letters

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

    # convert % encoded passwords as utf-8 characters
    special = ['!', '@', '#', '$', '^', '&', '(', ')', '-', '_', '=', '%'];
    encodings = ['%21', '%40', '%23', '%24', '%5E', '%26', '%28', '%29', '%2D', '%5F', '%3D', '%25'];
    for x in range(len(special)):
        pwd.replace(special[x], encodings[x]);
    # return the parsed credentials as list
    credentials = [user, pwd];
    return credentials;

def validate_password(str):
    if len(str) < 8:
        return False;

    # check for upper and lowercase characters and num and special
    contains_lower = False;
    contains_upper = False;
    contains_num = False;
    contains_special = False;

    digits = {0,1,2,3,4,5,6,7,8,9};
    special = {'!', '@', '#', '$', '^', '&', '(', ')', '-', '_', '=', '%'};

    for char in str:
        if contains_lower == False and char in ascii_lowercase:
            contains_lower = True;
        if contains_upper == False and char in ascii_uppercase:
            contains_upper = True;
        if contains_num == False and char in digits:
            contains_num = True;
        if contains_special == False and char in special:
            contains_special = True;
        if char not in ascii_letters and char not in digits and char not in special:
            return False;
    if not contains_lower or not contains_upper or not contains_num:
        return False;

    pass

