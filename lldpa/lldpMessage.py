from lldpa.tlvs import base
from lldpa.tlvs import chassisId
from lldpa.tlvs import eolldpdu
from lldpa.tlvs import portId
from lldpa.tlvs import ttl
from lldpa.lldpExceptions import *
import binascii
class LLDPMessage(object):
    def __init__(self, src_mac=""):
        self.tlv_list = list()
        self.mac = src_mac

    def __getitem__(self, index):
        return self.tlv_list.__getitem__(index)

    def __str__(self):
        output = 'LLDPMessage(src_mac=' + self.mac + ','
        output += self.tlv_list.__getitem__(0).__str__() + ','
        output += self.tlv_list.__getitem__(1).__str__() + ','
        output += self.tlv_list.__getitem__(2).__str__() + ')'
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
        #print(hex_bytes_in)
        chassis_payload, new_hex, temp_ty = self.extract(hex_bytes_in)
        if temp_ty == 1:
            new_tlv = chassisId.TLVChassisId()
            new_tlv.load(binascii.unhexlify(chassis_payload))
            self.tlv_list.append(new_tlv)
        else:
            raise ImproperTLVOrderException(1, temp_ty)
        hex_bytes_in = new_hex
        #print(hex_bytes_in)

        port_payload, new_hex, temp_ty = self.extract(hex_bytes_in)
        if temp_ty == 2:
            new_tlv = portId.TLVPortId()
            new_tlv.load(binascii.unhexlify(port_payload))
            self.tlv_list.append(new_tlv)
        else:
            raise ImproperTLVOrderException(2, temp_ty)
        hex_bytes_in = new_hex
        #print(hex_bytes_in)

        ttl_payload, new_hex, temp_ty = self.extract(hex_bytes_in)
        if temp_ty == 3:
            new_tlv = ttl.TLVTTL()
            new_tlv.load(binascii.unhexlify(ttl_payload))
            self.tlv_list.append(new_tlv)
        else:
            raise ImproperTLVOrderException(3, temp_ty)
        hex_bytes_in = new_hex
        #print(hex_bytes_in)

        while len(hex_bytes_in) > 0:
            #print(len(hex_bytes_in))
            #print(hex_bytes_in)
            payload, new_hex, temp_ty = self.extract(hex_bytes_in)
            #print("--")
            #print(payload)
            #print(temp_ty)
            if temp_ty == 0:
                self.tlv_list.append(eolldpdu.TVLEoLLDPDU())
                return
            elif temp_ty == 4 or temp_ty == 5 or temp_ty == 6 or temp_ty == 7 or temp_ty == 8 or temp_ty == 127:
                new_tlv = base.LLDPTLV(temp_ty, "", 0)
                new_tlv.load(binascii.unhexlify(payload))
                self.tlv_list.append(new_tlv)
            else:
                raise OptionalTLVTypeOutOfRangeException(temp_ty)
            hex_bytes_in = new_hex
        raise Exception("Missing EOL")


    def dump(self):
        """Dumps all TLVs of the message"""
        dump = bytearray()
        for x in self.tlv_list:
            dump += x.dump()
        return dump

    def extract(self, data):
        tl_string = bin(int(data[0:4], 16))[2:].zfill(16)
        ty = int(tl_string[0:7].zfill(16), 2)
        le = int(tl_string[7:16].zfill(16), 2)
        return data[0:le*2+4], data[le*2+4:], ty
