from lldpa.tlvs import base
from lldpa.lldpExceptions import EoLLDPDUNotEmptyException
import binascii


class TVLEoLLDPDU(base.LLDPTLV):
    def __init__(self):
        self.tlv_type2 = 0
        self.length2 = 0
        self.value = ""

    def __str__(self):
        """Return a string representation of the TLV"""
        return ""

    def load(self, bytes_in):
        temp = binascii.hexlify(bytes_in)
        if temp != '0000':
            raise EoLLDPDUNotEmptyException("0x" + temp)

    def dump(self):
        return binascii.unhexlify('0000')
