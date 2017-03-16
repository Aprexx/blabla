from lldpa.tlvs import base


class TLVChassisId(base.LLDPTLV):
    def __init__(self, sub_type=0, chassis_id=""):
        pass  # TODO: Implement.

    def __str__(self):
        """Return a string representation of the TLV"""
        return ""  # TODO: Implement.

    def load(self, bytes_in):
        pass  # TODO: Implement.

    def dump(self):
        return bytearray()  # TODO: Implement.

    def chassis_id(self):
        return ""  # TODO: Implement.

    def sub_type(self):
        return 0  # TODO: Implement.
