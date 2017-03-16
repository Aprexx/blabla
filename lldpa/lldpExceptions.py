class LLDPParseException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "LLDPParseException"


class ImproperDestinationMACException(LLDPParseException):
    def __init__(self, dst_mac):
        self.dst_mac = dst_mac

    def __str__(self):
        return "Improper Destination MAC: " + self.dst_mac + " Expected: 01:80:c2:00:00:0e or 01:80:c2:00:00:03 or " \
                                                             "01:80:c2:00:00:00\n"


class EoLLDPDUNotEmptyException(LLDPParseException):
    def __init__(self, eol):
        self.eol = eol

    def __str__(self):
        return "EoLLDPDU is not empty. Expected: 0x0000 Was: " + self.eol + "\n"


class OptionalTLVTypeOutOfRangeException(LLDPParseException):
    def __init__(self, tlv_type):
        self.tlv_type = tlv_type

    def __str__(self):
        return "Optional TLV Type out of range. Expected: 4-8 or 127. Was: " + self.tlv_type + "\n"


class ImproperTLVOrderException(LLDPParseException):
    def __init__(self, tlv_type_expected, tlv_type_was):
        self.tlv_type_expected = tlv_type_expected
        self.tlv_type_was = tlv_type_was

    def __str__(self):
        return "Improper TLV Order. Expected: " + self.tlv_type_expected + " Was: " + self.tlv_type_was + "\n"


class OwnMessageException(LLDPParseException):
    def __init__(self):
        pass

    def __str__(self):
        return "Ignoring own message\n"
