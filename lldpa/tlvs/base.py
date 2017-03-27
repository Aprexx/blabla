class LLDPTLV(object):
    def __init__(self, tlv_type, value, length=0):
        """Constructor"""

        print("finally")
        pass  # TODO: Implement.

    def load(self, bytes_in):
        """Load TLV from raw bytes

        Reads type, length and value from the input bytearray

        The first 7 bits are the type
        The next 9 bits are the length
        The next 0-511 bytes are the value

        :rtype: None
        """
        pass  # TODO: Implement.

    def dump(self):
        """Dump TLV into raw bytes

        Returns type, length and value as a bytearray

        :rtype: bytearray
        """
        return bytearray()  # TODO: Implement.

    def _type(self):
        """The TLV Type"""
        return 0  # TODO: Implement.

    def type_bytes(self):
        """Return the TLV type as bytes"""
        return bytearray()  # TODO: Implement.

    def _length(self):
        """The TLV Length"""
        return 0  # TODO: Implement.

    def length_bytes(self):
        """Return the TLV length as bytes"""
        return bytearray()  # TODO: Implement.

    def value_bytes(self):
        """Return the TLV value as bytes"""
        return bytearray()  # TODO: Implement.

    def __getattr__(self, item):
        if item == "type":
            return self._type()
        elif item == "length":
            return self._length()
