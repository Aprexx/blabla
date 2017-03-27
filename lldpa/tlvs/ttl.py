from lldpa.tlvs import base


class TLVTTL(base.LLDPTLV):
    def __init__(self, ttl=100):
        self.ttl = ttl

    def __str__(self):
        """Return a string representation of the TLV"""
        return ""  # TODO: Implement.

    def load(self, bytes_in):
        pass  # TODO: Implement

    def dump(self):
        return bytearray()  # TODO: Implement

    def ttl(self):
        return 0  # TODO: Implement.
