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

    # array = bytearray(bytes)

    # print("Calling set_fin once: ")
    parsed.set_fin(bytes)
    # print(parsed.fin_bit)

    # print("Calling set_opcode once: ")
    parsed.set_opcode(bytes)
    # print(parsed.opcode)

    # print("Calling set_len once: ")
    parsed.set_len(bytes)
    # print(parsed.payload_length)

    # print("Calling set_payload once: ")
    parsed.set_payload(bytes)
    # print(parsed.payload)

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
        if payload_length >= 65536:
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

        # absolutely stupid thing here where bitshifting 0 right turns it into a 0
        # nvm, order of operations

        # print(bytes[0])
        # print(bytes[0] & 0b10000000)
        # print((bytes[0] & 0b10000000) >> 7)
        self.fin_bit = int((bytes[0] & 0b10000000) >> 7)
        # print(self.fin_bit)

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
                num = bytes[2:4]
                self.payload_length = int.from_bytes(num, "big")
                # print(self.payload_length)
            # if 127, read next 8 bytes
            if self.payload_length == 127:
                num = bytes[2:10]
                self.payload_length = int.from_bytes(num, "big")
    
    def set_payload(self, bytes):
        # find if mask exists by masking first len byte with 10000000
        if int(bytes[1] &0x80) == 128:
            # get mask after length bytes
            mask_list = []
            mask_start = 0
            first_len_byte = int(bytes[1] & 0b01111111)
            if first_len_byte == 126:
                mask_start = 4
            elif first_len_byte == 127:
                mask_start = 10
            else:
                mask_start = 2
            payload_start = mask_start + 4
            for byte in bytes[mask_start:payload_start]:
                # print("Found Mask Bit: ")
                # print(byte)
                mask_list.append(byte)
                
            # print(mask_list)
            # get payload after mask bytes
            payload_array = bytes[payload_start:]
            # print(payload_array)
            # print(len(payload_array))
            # for every four bytes of payload, XOR with each byte of mask
            # neat(?) way, copy all payload bytes to another array, use modulo to determine which mask byte to XOR by
            i = 0
            for byte in payload_array:
                # print("Iteration: " + str(i))
                # print("Current byte in payload: ")
                # print(byte)
                # print("Current mask bit: ")
                # print(mask_list[i % 4])
                # print("XOR'd out with mask bit: ")
                # print(byte ^ mask_list[i % 4])
                xored_byte = byte ^ mask_list[i % 4]
                # print("Payload is: ")
                # print(self.payload)
                self.payload = self.payload + xored_byte.to_bytes(1,"big")
                # print("Updated Payload is: ")
                # print(self.payload)
                i = i + 1
        else:
            # get payload after length bytes
            # basically just add bytes up to length to payload
            # mask doesn't exist so don't need to get 4 at a time
            payload_start = 0
            first_len_byte = int(bytes[1] & 0b01111111)
            if first_len_byte == 126:
                payload_start = 4
            elif first_len_byte == 127:
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

# test short without mask
def test3():
    bytes = b'\x81\x02\x68\x69'
    parsed = parse_ws_frame(bytes)

    expected_len = 2
    actual_len = parsed.payload_length
    # print(actual_len)

    expected_fin = 1
    actual_fin = parsed.fin_bit
    # print(actual_fin)

    expected_opcode = 1
    actual_opcode = parsed.opcode
    # print(actual_opcode)

    expected_payload = b'hi'
    actual_payload = parsed.payload
    # print(actual_payload)

    assert expected_len == actual_len
    assert expected_fin == actual_fin
    assert expected_opcode == actual_opcode
    assert expected_payload == actual_payload

# test parse short with mask
def test4():
    bytes = b'\x01\x82\x08\x09\x0A\x0B\x60\x60'
    parsed = parse_ws_frame(bytes)
    # parsed.set_fin(bytes)
    # parsed.set_opcode(bytes)
    # parsed.set_len(bytes)
    # parsed.set_payload(bytes)

    expected_len = 2
    actual_len = parsed.payload_length
    # print(actual_len)

    expected_fin = 0
    actual_fin = parsed.fin_bit
    # print(actual_fin)

    expected_opcode = 1
    actual_opcode = parsed.opcode
    # print(actual_opcode)

    expected_payload = b'hi'
    actual_payload = parsed.payload
    # print("Payload is: ")
    # print(actual_payload)

    assert expected_len == actual_len
    assert expected_fin == actual_fin
    assert expected_opcode == actual_opcode
    assert expected_payload == actual_payload

def test5():
    bytes = b'\x81\x7E\x04\xD6\x34\x31\x20\x36\x33\x20\x36\x33\x20\x36\x66\x20\x37\x32\x20\x36\x34\x20\x36\x39\x20\x36\x65\x20\x36\x37\x20\x32\x30\x20\x37\x34\x20\x36\x66\x20\x32\x30\x20\x36\x31\x20\x36\x63\x20\x36\x63\x20\x32\x30\x20\x36\x62\x20\x36\x65\x20\x36\x66\x20\x37\x37\x20\x36\x65\x20\x32\x30\x20\x36\x63\x20\x36\x31\x20\x37\x37\x20\x37\x33\x20\x32\x30\x20\x36\x66\x20\x36\x36\x20\x32\x30\x20\x36\x31\x20\x37\x36\x20\x36\x39\x20\x36\x31\x20\x37\x34\x20\x36\x39\x20\x36\x66\x20\x36\x65\x20\x32\x63\x20\x32\x30\x20\x37\x34\x20\x36\x38\x20\x36\x35\x20\x37\x32\x20\x36\x35\x20\x32\x30\x20\x36\x39\x20\x37\x33\x20\x32\x30\x20\x36\x65\x20\x36\x66\x20\x32\x30\x20\x37\x37\x20\x36\x31\x20\x37\x39\x20\x32\x30\x20\x36\x31\x20\x32\x30\x20\x36\x32\x20\x36\x35\x20\x36\x35\x20\x32\x30\x20\x37\x33\x20\x36\x38\x20\x36\x66\x20\x37\x35\x20\x36\x63\x20\x36\x34\x20\x32\x30\x20\x36\x32\x20\x36\x35\x20\x32\x30\x20\x36\x31\x20\x36\x32\x20\x36\x63\x20\x36\x35\x20\x32\x30\x20\x37\x34\x20\x36\x66\x20\x32\x30\x20\x36\x36\x20\x36\x63\x20\x37\x39\x20\x32\x65\x20\x30\x61\x20\x34\x39\x20\x37\x34\x20\x37\x33\x20\x32\x30\x20\x37\x37\x20\x36\x39\x20\x36\x65\x20\x36\x37\x20\x37\x33\x20\x32\x30\x20\x36\x31\x20\x37\x32\x20\x36\x35\x20\x32\x30\x20\x37\x34\x20\x36\x66\x20\x36\x66\x20\x32\x30\x20\x37\x33\x20\x36\x64\x20\x36\x31\x20\x36\x63\x20\x36\x63\x20\x32\x30\x20\x37\x34\x20\x36\x66\x20\x32\x30\x20\x36\x37\x20\x36\x35\x20\x37\x34\x20\x32\x30\x20\x36\x39\x20\x37\x34\x20\x37\x33\x20\x32\x30\x20\x36\x36\x20\x36\x31\x20\x37\x34\x20\x32\x30\x20\x36\x63\x20\x36\x39\x20\x37\x34\x20\x37\x34\x20\x36\x63\x20\x36\x35\x20\x32\x30\x20\x36\x32\x20\x36\x66\x20\x36\x34\x20\x37\x39\x20\x32\x30\x20\x36\x66\x20\x36\x36\x20\x36\x36\x20\x32\x30\x20\x37\x34\x20\x36\x38\x20\x36\x35\x20\x32\x30\x20\x36\x37\x20\x37\x32\x20\x36\x66\x20\x37\x35\x20\x36\x65\x20\x36\x34\x20\x32\x65\x20\x30\x61\x20\x35\x34\x20\x36\x38\x20\x36\x35\x20\x32\x30\x20\x36\x32\x20\x36\x35\x20\x36\x35\x20\x32\x63\x20\x32\x30\x20\x36\x66\x20\x36\x36\x20\x32\x30\x20\x36\x33\x20\x36\x66\x20\x37\x35\x20\x37\x32\x20\x37\x33\x20\x36\x35\x20\x32\x63\x20\x32\x30\x20\x36\x36\x20\x36\x63\x20\x36\x39\x20\x36\x35\x20\x37\x33\x20\x32\x30\x20\x36\x31\x20\x36\x65\x20\x37\x39\x20\x37\x37\x20\x36\x31\x20\x37\x39\x20\x32\x30\x20\x36\x32\x20\x36\x35\x20\x36\x33\x20\x36\x31\x20\x37\x35\x20\x37\x33\x20\x36\x35\x20\x32\x30\x20\x36\x32\x20\x36\x35\x20\x36\x35\x20\x37\x33\x20\x32\x30\x20\x36\x34\x20\x36\x66\x20\x36\x65\x20\x32\x37\x20\x37\x34\x20\x32\x30\x20\x36\x33\x20\x36\x31\x20\x37\x32\x20\x36\x35\x20\x32\x30\x20\x37\x37\x20\x36\x38\x20\x36\x31\x20\x37\x34\x20\x32\x30\x20\x36\x38\x20\x37\x35\x20\x36\x64\x20\x36\x31\x20\x36\x65\x20\x37\x33\x20\x32\x30\x20\x37\x34\x20\x36\x38\x20\x36\x39\x20\x36\x65\x20\x36\x62\x20\x32\x30\x20\x36\x39\x20\x37\x33\x20\x32\x30\x20\x36\x39\x20\x36\x64\x20\x37\x30\x20\x36\x66\x20\x37\x33\x20\x37\x33\x20\x36\x39\x20\x36\x32\x20\x36\x63\x20\x36\x35\x20\x32\x65\x20\x30\x61\x20\x35\x39\x20\x36\x35\x20\x36\x63\x20\x36\x63\x20\x36\x66\x20\x37\x37\x20\x32\x63\x20\x32\x30\x20\x36\x32\x20\x36\x63\x20\x36\x31\x20\x36\x33\x20\x36\x62\x20\x32\x65\x20\x32\x30\x20\x35\x39\x20\x36\x35\x20\x36\x63\x20\x36\x63\x20\x36\x66\x20\x37\x37\x20\x32\x63\x20\x32\x30\x20\x36\x32\x20\x36\x63\x20\x36\x31\x20\x36\x33\x20\x36\x62\x20\x32\x65\x20\x32\x30\x20\x35\x39\x20\x36\x35\x20\x36\x63\x20\x36\x63\x20\x36\x66\x20\x37\x37\x20\x32\x63\x20\x32\x30\x20\x36\x32\x20\x36\x63\x20\x36\x31\x20\x36\x33\x20\x36\x62\x20\x32\x65\x20\x32\x30\x20\x35\x39\x20\x36\x35\x20\x36\x63\x20\x36\x63\x20\x36\x66\x20\x37\x37\x20\x32\x63\x20\x32\x30\x20\x36\x32\x20\x36\x63\x20\x36\x31\x20\x36\x33\x20\x36\x62\x20\x32\x65\x20\x30\x61\x20\x34\x66\x20\x36\x66\x20\x36\x38\x20\x32\x63\x20\x32\x30\x20\x36\x32\x20\x36\x63\x20\x36\x31\x20\x36\x33\x20\x36\x62\x20\x32\x30\x20\x36\x31\x20\x36\x65\x20\x36\x34\x20\x32\x30\x20\x37\x39\x20\x36\x35\x20\x36\x63\x20\x36\x63\x20\x36\x66\x20\x37\x37\x20\x32\x31\x20\x30\x61\x20\x34\x63\x20\x36\x35\x20\x37\x34\x20\x32\x37\x20\x37\x33\x20\x32\x30\x20\x37\x33\x20\x36\x38\x20\x36\x31\x20\x36\x62\x20\x36\x35\x20\x32\x30\x20\x36\x39\x20\x37\x34\x20\x32\x30\x20\x37\x35\x20\x37\x30\x20\x32\x30\x20\x36\x31\x20\x32\x30\x20\x36\x63\x20\x36\x39\x20\x37\x34\x20\x37\x34\x20\x36\x63\x20\x36\x35\x20\x32\x65\x20\x30\x61\x20\x34\x32\x20\x36\x31\x20\x37\x32\x20\x37\x32\x20\x37\x39\x20\x32\x31\x20\x32\x30\x20\x34\x32\x20\x37\x32\x20\x36\x35\x20\x36\x31\x20\x36\x62\x20\x36\x36\x20\x36\x31\x20\x37\x33\x20\x37\x34\x20\x32\x30\x20\x36\x39\x20\x37\x33\x20\x32\x30\x20\x37\x32\x20\x36\x35\x20\x36\x31\x20\x36\x34\x20\x37\x39\x20\x32\x31\x20\x30\x61\x20\x34\x33\x20\x36\x66\x20\x36\x64\x20\x36\x39\x20\x36\x65\x20\x36\x37\x20\x32\x31\x20\x30\x61\x20\x34\x38\x20\x36\x31\x20\x36\x65\x20\x36\x37\x20\x32\x30\x20\x36\x66\x20\x36\x65\x20\x32\x30\x20\x36\x31\x20\x32\x30\x20\x37\x33\x20\x36\x35\x20\x36\x33\x20\x36\x66\x20\x36\x65\x20\x36\x34\x20\x32\x65\x20\x30\x61\x20\x34\x38\x20\x36\x35\x20\x36\x63\x20\x36\x63\x20\x36\x66\x20\x33\x66'
    parsed = parse_ws_frame(bytes)
    # print(parsed.fin_bit)
    # print(parsed.opcode)
    # print(parsed.payload_length)
    # print(parsed.payload)

def test6():
    bytes = b"\x81\x7E\x04\xD6According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready! Coming! Hang on a second. Hello?"
    parsed = parse_ws_frame(bytes)
    actual_fin = parsed.fin_bit
    actual_opcode = parsed.opcode
    actual_len = parsed.payload_length
    actual_payload = parsed.payload
    expected_len = 1238
    expected_fin = 1
    expected_opcode = 1
    expected_payload = b"According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready! Coming! Hang on a second. Hello?"

    assert expected_fin == actual_fin
    assert expected_opcode == actual_opcode
    assert expected_len == actual_len
    assert expected_payload == actual_payload

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()




