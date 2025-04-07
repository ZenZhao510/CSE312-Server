import hashlib
import base64

def compute_accept(key):
    # append the magic key to key
    MAGIC = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    to_hash = key.encode() + MAGIC

    hashed = hashlib.sha1(to_hash).hexdigest()
    # print(hashed)
    ret = base64.b64encode(hashed.encode())

    return ret

def parse_ws_frame(bytes):
    parsed = WS_Frame(bytes)
    
    

    return parsed

class WS_Frame:

    def __init__(self, bytes):
        self.fin_bit = 0
        self.opcode = 0
        self.payload_length = 0
        self.payload = b""
    
    def 

def test1():
    key = "hi"
    # 25717a597d0c0749a666972bc8168397c69de035
    expected = b"MjU3MTdhNTk3ZDBjMDc0OWE2NjY5NzJiYzgxNjgzOTdjNjlkZTAzNQ=="
    actual = compute_accept(key)
    # print(actual)
    assert expected == actual

if __name__ == '__main__':
    test1()




