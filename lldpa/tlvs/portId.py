from lldpa.tlvs import base


class TLVPortId(base.LLDPTLV):
    def __init__(self, sub_type=0, port_id=""):
        pass  # TODO: Implement.

    def __str__(self):
        """Return a string representation of the TLV"""
        return ""  # TODO: Implement.

    def load(self, bytes_in):
        pass  # TODO: Implement.

    def dump(self):
        return bytearray()  # TODO: Implement.

    def sub_type(self):
        return 0  # TODO: Implement.

    def port_id(self):
        return 0  # TODO: Implement.
