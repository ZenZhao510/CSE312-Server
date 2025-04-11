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

    array = bytearray(bytes)
    parsed.fin_bit = parsed.set_fin(array)
    parsed.opcode = parsed.set_opcode(array)
    parsed.payload_length = parsed.set_len(array)
    parsed.payload = parsed.set_payload(array)

    return parsed

def generate_ws_frame(bytes):
    pass

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
        self.opcode = int(bytes[0] & 0b000010000)
    
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
                i += 1
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
    key = "hi"
    # 25717a597d0c0749a666972bc8168397c69de035
    expected = b"MjU3MTdhNTk3ZDBjMDc0OWE2NjY5NzJiYzgxNjgzOTdjNjlkZTAzNQ=="
    actual = compute_accept(key)
    # print(actual)
    assert expected == actual

if __name__ == '__main__':
    test1()




