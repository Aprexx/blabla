from lldpa.tlvs import base
import binascii
import struct


class TLVChassisId(base.LLDPTLV):
    def __init__(self, sub_type=0, chassis_id=""):
        self.sub_type2 = sub_type
        self.chassis_id2 = chassis_id
        self.tlv_type2 = 1
        self.length2 = 7
        self.value = '04' + chassis_id.replace(":", "")

    def __str__(self):
        """Return a string representation of the TLV"""
        return "chassis_id=" + self.chassis_id2

    def load(self, bytes_in):
        temp = binascii.hexlify(bytes_in)
        tl_string = bin(int(temp[0:4], 16))[2:].zfill(16)
        self.tlv_type2 = int(tl_string[0:7].zfill(16), 2)
        self.length2 = int(tl_string[7:16].zfill(16), 2)
        data = temp[4:]
        self.value = data
        if self.type == 1:
            if int(self.value[0:2], 16) == 4:
                self.sub_type2 = 4
                temp2 = self.value[2:]
                self.chassis_id2 = ':'.join([temp2[i:i+2] for i in range(0, len(temp2), 2)]).upper()
            else:
                print("not part of project")
        else:
            print("chassis type != 1")

    def dump(self):
        result = bytearray()
        result.append(struct.pack("!H", self.type << 1)[1:2])
        result.append(struct.pack("!H", self.length)[1:2])
        result.append(struct.pack("B", self.sub_type2))
        result.extend(binascii.unhexlify(self.chassis_id2.replace(":", "")))
        return result

    def chassis_id(self):
        return self.chassis_id2

    def sub_type(self):
        return self.sub_type2
