from lldpa.tlvs import base


class TVLEoLLDPDU(base.LLDPTLV):
    def __init__(self):
        pass  # TODO: Implement.

    def __str__(self):
        """Return a string representation of the TLV"""
        return ""  # TODO: Implement.

    def load(self, bytes_in):
        pass  # TODO: Implement.

    def dump(self):
        return bytearray()  # TODO: Implement.
