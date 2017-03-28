from struct import *
import binascii
class LLDPTLV(object):
    def __init__(self, tlv_type, value, length=0):
        """Constructor"""
        self.tlv_type = tlv_type
        self.value = value
        self.length = length


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
        self.tlv_type = int(tl_string[0:7].zfill(16), 2)
        self.length = int(tl_string[7:16].zfill(16), 2)
        self.value = temp[4:]


    def dump(self):
        """Dump TLV into raw bytes

        Returns type, length and value as a bytearray

        :rtype: bytearray
        """
        print("dump")
        print(bin(self.tlv_type))
        print(bin(self.length))
        head = hex(int(bin(self.tlv_type)[2:].zfill(8)[1:8] + bin(self.length)[2:].zfill(9)),2)[2:]
        print(head + self.value)
        return binascii.unhexlify(head + self.value)


    def _type(self):
        """The TLV Type"""
        return self.tlv_type

    def type_bytes(self):
        """Return the TLV type as bytes"""
        return pack('h', self.tlv_type)

    def _length(self):
        """The TLV Length"""
        return self.length

    def length_bytes(self):
        """Return the TLV length as bytes"""
        return pack('i', self.length)

    def value_bytes(self):
        """Return the TLV value as bytes"""
        return binascii.unhexlify(self.value)

    def __getattr__(self, item):
        if item == "type":
            return self._type()
        elif item == "length":
            return self._length()
