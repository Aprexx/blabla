from lldpa.tlvs import base
import binascii


class TLVTTL(base.LLDPTLV):
    def __init__(self, ttl=100):
        self.ttl = ttl
        self.tlv_type = 3
        self.length = 2

    def __str__(self):
        """Return a string representation of the TLV"""
        return "ttl=" + str(self.ttl)

    def load(self, bytes_in):
        temp = binascii.hexlify(bytes_in)
        tl_string = bin(int(temp[0:4], 16))[2:]
        self.tlv_type = int(tl_string[0:7].zfill(16), 2)
        self.length = int(tl_string[7:16].zfill(16), 2)
        data = temp[4:]
        if self.tlv_type == 3:
            if self.length == 2:
                self.ttl = int(data, 16)
            else:
                print("ttl length != 2")
        else:
            print("ttl type != 3")

    def dump(self):
        output = hex(int((bin(3)[2:].zfill(7) + bin(2)[2:].zfill(9) + bin(self.ttl)[2:].zfill(8)), 2))
        return binascii.unhexlify(output)

    def ttl(self):
        return self.ttl
