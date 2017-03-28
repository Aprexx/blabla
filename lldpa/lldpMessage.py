from lldpa.tlvs import *
import binascii
class LLDPMessage(object):
    def __init__(self, src_mac=""):
        self.tlv_list = list()
        self.mac = src_mac

    def __getitem__(self, index):
        return self.tlv_list.__getitem__(index)

    def __str__(self):
        output = 'LLDPMessage('

        return output

    def __repr__(self):
        return self.__str__()

    def append(self, tlv):
        """Appends a tlv to the list of tlvs"""
        self.tlv_list.append(tlv)

    def load(self, bytes_in):
        """Parses a byte stream. The first three TLVs MUST be (in this order):
        ChassisID TLV
        PortID TLV
        Time to live TLV

        The last TLV MUST be an End of LLDPDU TLV

        In between there can be optional TLVs

        :param bytes_in: The bytestream to parse
        :return: None
        """
        hex_bytes_in = binascii.hexlify(bytes_in)

        while len(hex_bytes_in)>0:
            tl_string = bin(int(hex_bytes_in[0:4], 16))[2:]
            type = int(tl_string[0:7].zfill(16), 2)
            length = int(tl_string[7:16].zfill(16), 2)
            end = length*2+2
            #chass = chassisId().load(hex_bytes_in[0:end])
            break

        return bytearray()  # TODO: Implement.

    def dump(self):
        """Dumps all TLVs of the message"""
        return bytearray()  # TODO: Implement.
