from lldpa.tlvs import base
import binascii
class LLDPMessage(object):
    tlv_list = list(base)
    def __init__(self, src_mac=""):
        pass  # TODO: Implement.

    def __getitem__(self, index):
        return None  # TODO: Implement.

    def __str__(self):
        return ""  # TODO: Implement.

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
        print("test")
        hex_bytes_in = binascii.hexlify(bytes_in)

        tl_string = bin(int(hex_bytes_in[0:4], 16))[2:].zfill(16)
        type = tl_string[0:7]
        length = tl_string[7:16]
        print(type)
        print(length)

        return bytearray()  # TODO: Implement.

    def dump(self):
        """Dumps all TLVs of the message"""
        return bytearray()  # TODO: Implement.

    def get_tlv(self, bytes):