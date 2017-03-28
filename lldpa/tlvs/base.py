from struct import *
import binascii
import struct
class LLDPTLV(object):
    def __init__(self, tlv_type, value, length=0):
        """Constructor"""
        self.tlv_type2 = tlv_type
        self.value = value
        self.length2 = length


    def load(self, bytes_in):
        """Load TLV from raw bytes

        Reads type, length and value from the input bytearray

        The first 7 bits are the type
        The next 9 bits are the length
        The next 0-511 bytes are the value

        :rtype: None
        """
        temp = binascii.hexlify(bytes_in)
        tl_string = bin(int(temp[0:4], 16))[2:]
        self.tlv_type2 = int(tl_string[0:7].zfill(16), 2)
        self.length2 = int(tl_string[7:16].zfill(16), 2)
        self.value = temp[4:]


    def dump(self):
        """Dump TLV into raw bytes

        Returns type, length and value as a bytearray

        :rtype: bytearray
        """
        result = bytearray()
        result.append(struct.pack("!H", self.type << 1)[1:2])
        result.append(struct.pack("!H", self.length2)[1:2])
        result.extend(binascii.unhexlify(self.value))
        return result

    def _type(self):
        """The TLV Type"""
        return self.tlv_type2

    def type_bytes(self):
        """Return the TLV type as bytes"""
        return pack('!H', self.tlv_type2)

    def _length(self):
        """The TLV Length"""
        return self.length2

    def length_bytes(self):
        """Return the TLV length as bytes"""
        return pack('!H', self.length2)

    def value_bytes(self):
        """Return the TLV value as bytes"""
        return binascii.unhexlify(self.value)

    def __getattr__(self, item):
        if item == "type":
            return self._type()
        elif item == "length":
            return self._length()
