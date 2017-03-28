from lldpa.tlvs import base
import binascii


class TLVChassisId(base.LLDPTLV):
    def __init__(self, sub_type=0, chassis_id=""):
        self.sub_type = sub_type
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
        tl_string = bin(int(temp[0:4], 16))[2:]
        self.tlv_type = int(tl_string[0:7].zfill(16), 2)
        self.length = int(tl_string[7:16].zfill(16), 2)
        data = temp[4:]
        if self.tlv_type == 1:
            if int(data[0:2], 16) == 4:
                self.sub_type = 4
                self.chassis_id = data[2:6] + ":" + data[6:10] + ":" + data[10:14]
            else:
                print("chassis subtype != 4")
        else:
            print("chassis type != 1")

    def dump(self):
        output = hex(int((bin(1)[2:].zfill(8)[1:] + bin(7)[2:].zfill(9) + bin(4)[2:].zfill(8)), 2))
        output += self.chassis_id.replace(":", "")
        return binascii.unhexlify(output)

    def chassis_id(self):
        return self.chassis_id

    def sub_type(self):
        return self.sub_type
