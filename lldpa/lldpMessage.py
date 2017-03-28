from lldpa.tlvs import base
from lldpa.tlvs import chassisId
from lldpa.tlvs import eolldpdu
from lldpa.tlvs import portId
from lldpa.tlvs import ttl
import binascii
class LLDPMessage(object):
    def __init__(self, src_mac=""):
        self.tlv_list = list()
        self.mac = src_mac

    def __getitem__(self, index):
        return self.tlv_list.__getitem__(index)

    def __str__(self):
        output = 'LLDPMessage('

        return output

    def __repr__(self):
        return self.__str__()

    def append(self, tlv):
        """Appends a tlv to the list of tlvs"""
        self.tlv_list.append(tlv)

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
        hex_bytes_in = binascii.hexlify(bytes_in)

        chassis_payload, new_hex, temp_ty = self.extract(hex_bytes_in)
        if temp_ty == 1:
            self.tlv_list.append(chassisId.TLVChassisId.load(chassis_payload))
        else:
            print("wrong tlv order")
        hex_bytes_in = new_hex

        port_payload, new_hex, temp_ty = self.extract(hex_bytes_in)
        if temp_ty == 2:
            self.tlv_list.append(portId.TLVPortId.load(port_payload))
        else:
            print("wrong tlv order")
        hex_bytes_in = new_hex

        ttl_payload, new_hex, temp_ty = self.extract(hex_bytes_in)
        if temp_ty == 3:
            self.tlv_list.append(ttl.TLVTTL.load(chassis_payload))
        else:
            print("wrong tlv order")

        while len(hex_bytes_in) > 0:
            payload, new_hex, temp_ty = self.extract(hex_bytes_in)
            if temp_ty == 0:
                self.tlv_list.append(eolldpdu.TVLEoLLDPDU())
                break
            else:
                self.tlv_list.append(base.LLDPTLV)
            hex_bytes_in = new_hex


        return bytearray()

    def dump(self):
        """Dumps all TLVs of the message"""
        return bytearray()  # TODO: Implement.

    def extract(self, data):
        tl_string = bin(int(data[0:4], 16))[2:].zfill(16)
        ty = int(tl_string[0:7].zfill(16), 2)
        le = int(tl_string[7:16].zfill(16), 2)
        return data[0:le*2+4], data[le*2+4:], ty
