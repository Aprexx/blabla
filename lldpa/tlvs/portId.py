from lldpa.tlvs import base
import binascii
import struct

class TLVPortId(base.LLDPTLV):
    def __init__(self, sub_type=0, port_id=""):
        self.sub_type2 = sub_type
        self.port_id2 = port_id
        self.tlv_type2 = 2
        if self.sub_type2 == 3:
            self.length2 = 7
            self.value = '03' + port_id.replace(":", "")
        if self.sub_type2 == 7:
            self.length2 = 1 + len(self.port_id2)
            self.value = '07' + port_id.encode("hex")

    def __str__(self):
        """Return a string representation of the TLV"""
        return "port_id=" + self.port_id2

    def load(self, bytes_in):
        temp = binascii.hexlify(bytes_in)
        tl_string = bin(int(temp[0:4], 16))[2:]
        self.tlv_type2 = int(tl_string[0:7].zfill(16), 2)
        self.length2 = int(tl_string[7:16].zfill(16), 2)
        self.value = temp[4:]
        if self.type == 2:
            if int(self.value[0:2], 16) == 3:
                self.port_id2 = self.value[2:6] + ":" + self.value[6:10] + ":" + self.value[10:14]
            elif int(self.value[0:2], 16) == 7:
                self.port_id2 = self.value[2:].decode("hex")
            else:
                print("port subtype != 3 or 7")
        else:
            print("port type != 2")

    def dump(self):
        # if self.sub_type == 3:
        #     output = hex(int((bin(2)[2:].zfill(7) + bin(7)[2:].zfill(9) + bin(3)[2:].zfill(8)), 2))
        #     output += self.port_id.replace(":", "")
        #     return binascii.unhexlify(output)
        # elif self.sub_type == 7:
        #     output = hex(int((bin(2)[2:].zfill(7) + bin(1+len(self.port_id))[2:].zfill(9) + bin(7)[2:].zfill(8)), 2))
        #     for x in self.port_id:
        #         output += x.encode('hex')
        #     return binascii.unhexlify(output)
        # else:
        #     print("port dump error")

        result = bytearray()
        result.append(struct.pack("!H", self.type << 1)[1:2])
        result.append(struct.pack("!H", self.length2)[1:2])
        result.append(struct.pack("B", self.sub_type()))
        # if self.sub_type() == 3:
        #     result.extend(binascii.unhexlify(self.port_id2.replace(":", "")))
        # if self.sub_type() == 7:
        #     for x in self.port_id():
        #         result.extend(x.encode("hex"))
        result.extend(binascii.unhexlify(self.value))

        return result

    def sub_type(self):
        return self.sub_type2

    def port_id(self):
        return self.port_id2
