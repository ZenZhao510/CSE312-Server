import hashlib
import base64

def compute_accept(key):
    # append the magic key to key
    MAGIC = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    to_hash = key.encode() + MAGIC
    # print(to_hash)
    hashed = hashlib.sha1(to_hash).digest()
    # print(hashed)
    ret = base64.b64encode(hashed)

    ret = ret.decode()
    return ret

def parse_ws_frame(bytes):
    parsed = WS_Frame(bytes)

    array = bytearray(bytes)
    parsed.fin_bit = parsed.set_fin(array)
    parsed.opcode = parsed.set_opcode(array)
    parsed.payload_length = parsed.set_len(array)
    parsed.payload = parsed.set_payload(array)

    return parsed

def generate_ws_frame(bytes):
    frame = b""
    fin_op = 0b10000001
    frame = frame + fin_op.to_bytes(1,"big")
    # print(frame)
    payload_length = len(bytes)
    if payload_length < 126:
        frame = frame + payload_length.to_bytes(1,"big")
        # print(frame)
    else:
        if payload_length < 65536:
            mask_len = 0b01111110
            frame = frame + mask_len.to_bytes(1,"big")
            frame = frame + payload_length.to_bytes(2,"big")
        if payload_length > 65536:
            mask_len = 0b01111111
            frame = frame + mask_len.to_bytes(1,"big")
            frame = frame + payload_length.to_bytes(8,"big")
    frame = frame + bytes
    return frame

class WS_Frame:

    def __init__(self, bytes):
        self.fin_bit = 0
        self.opcode = 0
        self.payload_length = 0
        self.payload = b""
    
    def set_fin(self, bytes):
        # get first bit of first byte 10000000
        self.fin_bit = int(bytes[0] & 0b10000000 >> 7)

    def set_opcode(self, bytes):
        # get second half of first byte 00001000
        self.opcode = int(bytes[0] & 0b00001111)
    
    def set_len(self, bytes):
        # grab length from byte 1 by masking it with 01111111
        self.payload_length = int(bytes[1] & 0b01111111)
        # if length ==126/127
        if self.payload_length > 125:
            # if 126, read next 2 bytes
            if self.payload_length == 126:
                self.payload_length = int(bytes[2:4])
                pass
            # if 127, read next 8 bytes
            if self.payload_length == 127:
                self.payload_length = int(bytes[2:10])
                pass
    
    def set_payload(self, bytes):
        # find if mask exists by masking first len byte with 10000000
        if int(bytes[1] & 0x80) == 128:
            # get mask after length bytes
            mask_list = []
            mask_start = 0
            if self.payload_length == 126:
                mask_start = 4
            elif self.payload_length == 127:
                mask_start = 10
            else:
                mask_start = 2
            payload_start = mask_start + 4
            for byte in bytes[mask_start:payload_start]:
                mask_list.append(byte)
            # get payload after mask bytes
            payload_array = bytes[payload_start:]

            # for every four bytes of payload, XOR with each byte of mask
            # neat(?) way, copy all payload bytes to another array, use modulo to determine which mask byte to XOR by
            i = 0
            for byte in payload_array:
                self.payload = byte ^ mask_list[i % 4]
                i = i + 1
        else:
            # get payload after length bytes
            # basically just add bytes up to length to payload
            # mask doesn't exist so don't need to get 4 at a time
            payload_start = 0
            if self.payload_length == 126:
                payload_start = 4
            elif self.payload_length == 127:
                payload_start = 10
            else:
                payload_start = 2
            self.payload = bytes[payload_start:]

def test1():
    key = "b/E7V80XDZJ95wuZ7JtBAw=="
    expected = "j126tKOHlnzCnfMSRKhlT7zLE38="
    actual = compute_accept(key)
    assert expected == actual

def test2():
    bytes = b"hi"
    actual = generate_ws_frame(b"hi")
    expected = b'\x81\x02hi'
    assert expected == actual

def test3():
    bytes = b'\x81\x02hi'
    parsed = parse_ws_frame(bytes)
    parsed.set_fin(bytes)
    parsed.set_opcode(bytes)
    parsed.set_len(bytes)
    parsed.set_payload(bytes)

    expected_len = 2
    actual_len = parsed.payload_length
    print(actual_len)

    expected_fin = 1
    actual_fin = parsed.fin_bit
    print(actual_fin)

    expected_opcode = 1
    actual_opcode = parsed.opcode
    print(actual_opcode)

    expected_payload = b'hi'
    actual_payload = parsed.payload
    print(actual_payload)

    assert expected_len == actual_len
    assert expected_fin == actual_fin
    assert expected_opcode == actual_opcode
    assert expected_payload == actual_payload

def test4():
    pass

if __name__ == '__main__':
    test1()
    test2()
    test3()




