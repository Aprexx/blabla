import unittest
import binascii
from lldpa.lldpExceptions import *
from lldpa.lldpMessage import LLDPMessage
from lldpa.tlvs import *
from lldpa.lldpAgent import LLDPAgent


class LLDPMessageTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_load(self):
        packet = b'\x02\x07\x04D\x8a[$\x0b\xeb\x04\x07\x03D\x8a[$\x0b\xeb\x06\x02\x0e\x11\x00\x00'

        msg = LLDPMessage("AB:CD:EF:01:23:45")
        msg.load(packet)

        self.assertEqual(msg[0].type, 1)
        self.assertEqual(msg[0].length, 7)
        self.assertEqual(msg[0].value_bytes(), b'\x04D\x8a[$\x0b\xeb')
        self.assertEqual(msg[1].type, 2)
        self.assertEqual(msg[1].length, 7)
        self.assertEqual(msg[1].value_bytes(), b'\x03D\x8a[$\x0b\xeb')
        self.assertEqual(msg[2].type, 3)
        self.assertEqual(msg[2].length, 2)
        self.assertEqual(msg[2].value_bytes(), b'\x0e\x11')
        self.assertEqual(msg[3].type, 0)
        self.assertEqual(msg[3].length, 0)

    def test_dump(self):
        msg = LLDPMessage("AB:CD:EF:01:23:45")
        msg.append(chassisId.TLVChassisId(sub_type=4, chassis_id="AB:CD:EF:01:23:45"))
        msg.append(portId.TLVPortId(sub_type=3, port_id="AB:CD:EF:01:23:45"))
        msg.append(ttl.TLVTTL(ttl=100))
        msg.append(eolldpdu.TVLEoLLDPDU())
        self.assertEqual(msg.dump(), b'\x02\x07\x04\xab\xcd\xef\x01\x23\x45\x04\x07\x03\xab\xcd\xef\x01\x23\x45\x06'
                                     b'\x02\x00\x64\x00\x00')

    def test_load_full_msg(self):
        full_msg = '0180c200000e80c16eb108df88cc02070480c16eb108c004020731060200780801310a1850726f4375727665205377697' \
                   '463682032353130422d32340c5450726f4375727665204a3930313942205377697463682032353130422d32342c207265' \
                   '766973696f6e20512e31312e35372c20524f4d20512e31302e303220282f73772f636f64652f6275696c642f686172702' \
                   '90e0400040004100c05010a0102030200000000000000'

        agent = LLDPAgent("eth0")

        msg = agent.parse_lldp_frame(binascii.unhexlify(full_msg))

        self.assertTrue(msg)

        chassis_id_tlv = msg[0]
        self.assertEqual(chassis_id_tlv.type, 1)
        self.assertEqual(chassis_id_tlv.length, 7)
        self.assertEqual(chassis_id_tlv.sub_type(), 4)
        self.assertEqual(chassis_id_tlv.chassis_id(), '80:C1:6E:B1:08:C0')

        port_id_tlv = msg[1]
        self.assertEqual(port_id_tlv.type, 2)
        self.assertEqual(port_id_tlv.length, 2)
        self.assertEqual(port_id_tlv.sub_type(), 7)
        self.assertEqual(int(port_id_tlv.port_id()), 1)

        ttl_tlv = msg[2]
        self.assertEqual(ttl_tlv.type, 3)
        self.assertEqual(ttl_tlv.length, 2)
        self.assertEqual(ttl_tlv.ttl(), 120)

        eol_tlv = msg[-1]
        self.assertEqual(eol_tlv.type, 0)
        self.assertEqual(eol_tlv.length, 0)

    def test_lldpdu(self):
        agent = LLDPAgent("")
        agent.src_mac = '@a\x86)\x82\xcc'

        self.assertEqual(agent.generate_lldpdu(),
                         b'\x02\x07\x04@a\x86)\x82\xcc\x04\x07\x03@a\x86)\x82\xcc\x06\x02\x00x\x00\x00'
                         b'')

    def test_parse_exception_tlv_order(self):
        full_msg = binascii.unhexlify('0180c200000e80c16eb108df88cc00070480c16eb108c0')

        agent = LLDPAgent("eth0")

        self.assertRaises(ImproperTLVOrderException, agent.parse_lldp_frame, full_msg)

    def test_parse_exception_missing_eol(self):
        full_msg = binascii.unhexlify('0180c200000e80c16eb108df88cc02070480c16eb108c00402073106020078')

        agent = LLDPAgent("eth0")

        self.assertRaises(Exception, agent.parse_lldp_frame, full_msg)

    def test_dst_mac_mismatch_exception(self):
        full_msg = binascii.unhexlify('1180c200000e80c16eb108df88cc00070480c16eb108c0')

        agent = LLDPAgent("eth0")

        self.assertRaises(ImproperDestinationMACException, agent.parse_lldp_frame, full_msg)

    def test_eol_not_empty_exception(self):
        full_msg = binascii.unhexlify('0180c200000e80c16eb108df88cc02070480c16eb108c004020731060200780001')

        agent = LLDPAgent("eth0")

        self.assertRaises(EoLLDPDUNotEmptyException, agent.parse_lldp_frame, full_msg)

    def test_optional_tlv_type_out_of_range_exception(self):
        full_msg = binascii.unhexlify('0180c200000e80c16eb108df88cc02070480c16eb108c004020731060200783c010000')

        agent = LLDPAgent("eth0")

        self.assertRaises(OptionalTLVTypeOutOfRangeException, agent.parse_lldp_frame, full_msg)

    def test_print_msg(self):
        msg = binascii.unhexlify('02070480c16eb108c004020731060200780000')

        message = LLDPMessage("01:23:45:67:89:AB")
        message.load(msg)

        self.assertEqual("LLDPMessage(src_mac=01:23:45:67:89:AB,chassis_id=80:C1:6E:B1:08:C0,port_id=1,ttl=120)",
                         message.__str__())
