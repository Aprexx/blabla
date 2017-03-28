from lldpa.tlvs import base
import binascii
import struct
import binascii

class TLVTTL(base.LLDPTLV):
    def __init__(self, ttl=100):
        self.ttl2 = ttl
        self.tlv_type2 = 3
        self.length2 = 2
        self.value = binascii.hexlify(struct.pack("!H", self.ttl()))

    def __str__(self):
        """Return a string representation of the TLV"""
        return "ttl=" + str(self.ttl)

    def load(self, bytes_in):
        temp = binascii.hexlify(bytes_in)
        tl_string = bin(int(temp[0:4], 16))[2:].zfill(16)
        self.tlv_type2 = int(tl_string[0:7].zfill(16), 2)
        self.length2 = int(tl_string[7:16].zfill(16), 2)
        self.value = temp[4:]
        if self.type == 3:
            if self.length == 2:
                self.ttl2 = int(self.value, 16)
            else:
                print("ttl length != 2")
        else:
            print("ttl type != 3")

    def dump(self):
        result = bytearray()
        result.append(struct.pack("!H", self.type << 1)[1:2])
        result.append(struct.pack("!H", self.length)[1:2])
        result.extend(struct.pack("!H", self.ttl()))
        return result

    def ttl(self):
        return self.ttl2
