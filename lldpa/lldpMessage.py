class LLDPMessage(object):

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
        pass  # TODO: Implement.

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

        return bytearray()  # TODO: Implement.

    def dump(self):
        """Dumps all TLVs of the message"""
        return bytearray()  # TODO: Implement.
