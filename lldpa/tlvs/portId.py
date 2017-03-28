from lldpa.tlvs import base
import binascii


class TLVPortId(base.LLDPTLV):
    def __init__(self, sub_type=0, port_id=""):
        self.sub_type = sub_type
        self.port_id = port_id

    def __str__(self):
        """Return a string representation of the TLV"""
        return "port_id=" + self.port_id

    def load(self, bytes_in):
        temp = binascii.hexlify(bytes_in)
        tl_string = bin(int(temp[0:4], 16))[2:]
        tlv_type = int(tl_string[0:7].zfill(16), 2)
        #  length = int(tl_string[7:16].zfill(16), 2)
        data = temp[4:]
        if tlv_type == 1:
            if int(data[0:2], 16) == 3:
                self.port_id = ':'.join([data[i:i+2] for i in range(2, len(data), 2)])
            elif int(data[0:2], 16) == 7:
                self.port_id = data[2:].decode("hex")
            else:
                print("port subtype != 3 or 7")
        else:
            print("port type != 2")

    def dump(self):
        if self.sub_type == 3:
            output = hex(int((bin(2)[2:].zfill(7) + bin(7)[2:].zfill(9) + bin(3)[2:].zfill(8)), 2))
            output += self.port_id.replace(":", "")
            return binascii.unhexlify(output)
        elif self.sub_type == 7:
            output = hex(int((bin(2)[2:].zfill(7) + bin(1+len(self.port_id))[2:].zfill(9) + bin(7)[2:].zfill(8)), 2))
            for x in self.port_id:
                output += x.encode('hex')
            return binascii.unhexlify(output)
        else:
            print("port dump error")

    def sub_type(self):
        return self.sub_type

    def port_id(self):
        return self.port_id
