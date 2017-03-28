from lldpa.tlvs import base
import binascii
import struct


class TLVChassisId(base.LLDPTLV):
    def __init__(self, sub_type=0, chassis_id=""):
        self.sub_type2 = sub_type
        if (sub_type != 4):
            print("chassis subtype != 4 cons")
        self.chassis_id = chassis_id
        self.tlv_type = 1
        self.length = 7

    def __str__(self):
        """Return a string representation of the TLV"""
        return "chassis_id=" + self.chassis_id

    def load(self, bytes_in):
        temp = binascii.hexlify(bytes_in)
        print(temp)
        tl_string = bin(int(temp[0:4], 16))[2:].zfill(16)
        print(tl_string)
        self.tlv_type = int(tl_string[0:7].zfill(16), 2)
        self.length = int(tl_string[7:16].zfill(16), 2)
        data = temp[4:]
        print(self.tlv_type)
        if self.tlv_type == 1:
            if int(data[0:2], 16) == 4:
                print("test")
                self.sub_type2 = 4
                self.chassis_id = data[2:6] + ":" + data[6:10] + ":" + data[10:14]
            else:
                print("chassis subtype != 4")
        else:
            print("chassis type != 1")

    def dump(self):
        # output = hex(int((bin(1)[2:].zfill(7) + bin(7)[2:].zfill(9) + bin(4)[2:].zfill(8)), 2))
        # output += self.chassis_id.replace(":", "")
        # print("huhuu")
        # print(output[2:].zfill(16))
        # return binascii.unhexlify(output[2:].zfill(16))
        result = bytearray()
        result.append(struct.pack("!H", self.tlv_type << 1)[1:2])
        result.append(struct.pack("!H", self.length)[1:2])
        result.append(struct.pack("B", self.sub_type2))
        result.extend(binascii.unhexlify(self.chassis_id.replace(":", "")))
        return result

    def chassis_id(self):
        return self.chassis_id

    def sub_type(self):
        return self.sub_type2
