# for some fucking reason autolab doesn't want me importing this, so i guess i have to comment out my tests just to submit thanks autolab
# oh it's probably because autolab needs util, but running tests locally i can't use util in path
# from request import Request
from string import ascii_lowercase
from string import ascii_uppercase
from string import ascii_letters

def extract_credentials(request):
    # print(request.body)
    query = request.body.decode()
    # print(query)
    # separate query parameters from rest of query
    query_list = query.split("&", 1) 
    # print(query_list)
    # should only need to splt once
    # separate parameter names from values
    user = query_list[0].split("=",1)[1]
    pwd = query_list[1].split("=",1)[1]

    # convert % encoded passwords as utf-8 characters
    special = ['!', '@', '#', '$', '^', '&', '(', ')', '-', '_', '=', '%']
    encodings = ['%21', '%40', '%23', '%24', '%5E', '%26', '%28', '%29', '%2D', '%5F', '%3D', '%25']
    for x in range(len(special)):
        pwd = pwd.replace(encodings[x], special[x])
    # return the parsed credentials as list
    credentials = [user, pwd]
    return credentials

def validate_password(str):
    if len(str) < 8:
        return False

    # check for upper and lowercase characters and num and special
    contains_lower = False
    contains_upper = False
    contains_num = False
    contains_special = False

    digits = {'0','1','2','3','4','5','6','7','8','9'}
    special = {'!', '@', '#', '$', '^', '&', '(', ')', '-', '_', '=', '%'}

    for char in str:
        if contains_lower == False and char in ascii_lowercase:
            # print("lw found: "+char)
            contains_lower = True
        if contains_upper == False and char in ascii_uppercase:
            # print("up found: "+char)
            contains_upper = True
        if contains_num == False and char in digits:
            # print("Num found: "+char)
            contains_num = True
        if contains_special == False and char in special:
            # print("Special found: "+char)
            contains_special = True
        if char not in ascii_lowercase and char not in ascii_uppercase and char not in digits and char not in special:
            return False
    if not contains_lower or not contains_upper or not contains_num or not contains_special:
        # print("no characters or num or special: "+str)
        return False

    return True

# def test1():
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=password')
    # credentials = extract_credentials(request)
    # assert credentials[0] == "Hi"
    # assert credentials[1] == "password"
# 
# def test2():
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=%21%40%23%24%5E%26%28%29%2D%5F%3D%25')
    # credentials = extract_credentials(request)
    # assert credentials[0] == "Hi"
    # assert credentials[1] == '!@#$^&()-_=%'
# 
# def test3():
    # # this would not be a valid request probably, as percent isn't percent-encoded, but this just means it's left untouched by extract_credentials since %11 isn't a supported special char
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=%21%40%23%24%5E%26%28%29%2D%5F%3D%25%11')
    # credentials = extract_credentials(request)
    # assert credentials[0] == "Hi"
    # assert credentials[1] == "!@#$^&()-_=%%11"
# 
# def test4():
    # # test to make sure percent doesn't fuck up 21 by turning it into !
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=%2521')
    # credentials = extract_credentials(request)
    # assert credentials[0] == "Hi"
    # assert credentials[1] == '%21'
# 
# 
# def test5():
    # # basic test with only lowercase
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=password')
    # credentials = extract_credentials(request)
    # assert validate_password(credentials[1]) is False
# 
# def test6():
    # # basic test with only UPPER
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=PASSWORD')
    # credentials = extract_credentials(request)
    # assert validate_password(credentials[1]) is False
# 
# def test7():
    # # basic test with only special
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=%21%40%23%24%5E%26%28%29%2D%5F%3D%25%11')
    # credentials = extract_credentials(request)
    # assert validate_password(credentials[1]) is False
# 
# def test8():
    # # basic test with only num
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=01234567890')
    # credentials = extract_credentials(request)
    # assert validate_password(credentials[1]) is False
# 
# def test9():
    # # basic test with too short
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=0%21aB')
    # credentials = extract_credentials(request)
    # assert validate_password(credentials[1]) is False
# 
# def test10():
    # # basic test with minimum viable password
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=Pass123%21')
    # credentials = extract_credentials(request)
    # assert validate_password(credentials[1]) is True
# 
# def test11():
    # # basic test with too short
    # request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\nusername=Hi&password=Password*23%21')
    # credentials = extract_credentials(request)
    # assert validate_password(credentials[1]) is False
# 
# if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    # test7()
    # test8()
    # test9()
    # test10()
    # test11()