import unittest
from lldpa.tlvs import ttl, chassisId, eolldpdu, portId
import struct
import binascii


class TLVTTLTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_create(self):
        ttl_time = 100
        tlv = ttl.TLVTTL(ttl=ttl_time)
        self.assertEqual(tlv.ttl(), ttl_time)

    def test_type(self):
        tlv = ttl.TLVTTL()
        self.assertTrue(tlv.type, 3)

    def test_value_length(self):
        ttl_time = 100
        length = 2
        tlv = ttl.TLVTTL(ttl=ttl_time)
        self.assertEqual(tlv.length_bytes(), struct.pack("!H", length))
        self.assertEqual(tlv.value_bytes(), struct.pack("!H", ttl_time))

    def test_dump(self):
        tlv_ttl_type = 3
        ttl_time = 100
        length = 2
        result = bytearray()
        result.append(struct.pack("!H", tlv_ttl_type << 1)[1:2])
        result.append(struct.pack("!H", length)[1:2])
        result.extend(struct.pack("!H", ttl_time))
        tlv = ttl.TLVTTL(ttl=ttl_time)
        self.assertEqual(tlv.dump(), result)

    def test_load(self):
        ttl_tlv_bytes = '\x06\x03\xF4\x24\x00'
        ttl_tlv = ttl.TLVTTL()
        ttl_tlv.load(ttl_tlv_bytes)
        self.assertEqual(ttl_tlv.ttl(), 16000000)


class TLVPortIdTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_create(self):
        subtype = 3
        mac = "AB:CD:EF:01:23:45"
        tlv = portId.TLVPortId(sub_type=subtype, port_id=mac)
        self.assertEqual(tlv.type, 2)
        self.assertEqual(tlv.sub_type(), subtype)
        self.assertEqual(tlv.port_id(), mac)

    def test_type(self):
        tlv = portId.TLVPortId()
        self.assertTrue(tlv.type, 2)

    def test_value_length(self):
        port_id = "AB:CD:EF:01:23:45"
        length = 7
        tlv = portId.TLVPortId(sub_type=3, port_id=port_id)
        self.assertEqual(tlv.length_bytes(), struct.pack("!H", length))
        self.assertEqual(tlv.value_bytes(), '\x03' + binascii.unhexlify(port_id.replace(':', '')))

    def test_dump(self):
        tlv_port_id_type = 2
        tlv_sub_type = 3
        port_id = "AB:CD:EF:01:23:45"
        port_id_hex = binascii.unhexlify(port_id.replace(':', ''))
        length = 7
        result = bytearray()
        result.append(struct.pack("!H", tlv_port_id_type << 1)[1:2])
        result.append(struct.pack("!H", length)[1:2])
        result.append(struct.pack("B", tlv_sub_type))
        result.extend(port_id_hex)
        tlv = portId.TLVPortId(sub_type=tlv_sub_type, port_id=port_id)
        self.assertEqual(tlv.dump(), result)

    def test_load(self):
        port_id_tlv_bytes = '\x04\x07\x03\xF4\x24\x00\xc8\x07\x11'
        port_id_tlv = portId.TLVPortId(sub_type=3, port_id="F4:24:00:C8:07:11")
        port_id_tlv.load(port_id_tlv_bytes)
        self.assertEqual(port_id_tlv.sub_type(), 3)
        self.assertEqual(port_id_tlv.port_id(), "F4:24:00:C8:07:11")


class TLVChassisIdTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_mac(self):
        subtype = 4
        mac = "AB:CD:EF:01:23:45"
        tlv = chassisId.TLVChassisId(sub_type=subtype, chassis_id=mac)
        self.assertEqual(tlv.type, 1)
        self.assertEqual(tlv.sub_type(), subtype)
        self.assertEqual(tlv.chassis_id(), mac)

    def test_create_if_alias(self):
        subtype = 2
        ifalias = "eth0"
        tlv = chassisId.TLVChassisId(sub_type=subtype, chassis_id=ifalias)
        self.assertEqual(tlv.sub_type(), subtype)
        self.assertEqual(tlv.chassis_id(), ifalias)

    def test_type(self):
        tlv = chassisId.TLVChassisId()
        self.assertTrue(tlv.type, 1)

    def test_value_length(self):
        chassis_id = "AB:CD:EF:01:23:45"
        length = 7
        tlv = chassisId.TLVChassisId(sub_type=4, chassis_id=chassis_id)
        self.assertEqual(tlv.length_bytes(), struct.pack("!H", length))
        self.assertEqual(tlv.value_bytes(), '\x04' + binascii.unhexlify(chassis_id.replace(':', '')))

    def test_dump(self):
        tlv_chassis_id_type = 1
        tlv_sub_type = 4
        chassis_id = "AB:CD:EF:01:23:45"
        chassis_id_hex = binascii.unhexlify(chassis_id.replace(':', ''))
        length = 7
        result = bytearray()
        result.append(struct.pack("!H", tlv_chassis_id_type << 1)[1:2])
        result.append(struct.pack("!H", length)[1:2])
        result.append(struct.pack("B", tlv_sub_type))
        result.extend(chassis_id_hex)
        tlv = chassisId.TLVChassisId(sub_type=tlv_sub_type, chassis_id=chassis_id)
        self.assertEqual(tlv.dump(), result)

    def test_load(self):
        chassis_id_tlv_bytes = '\x02\x07\x04\xF4\x24\x00\xc8\x07\x11'
        chassis_id_tlv = chassisId.TLVChassisId(sub_type=4, chassis_id="F4:24:00:C8:07:11")
        chassis_id_tlv.load(chassis_id_tlv_bytes)
        self.assertEqual(chassis_id_tlv.sub_type(), 4)
        self.assertEqual(chassis_id_tlv.chassis_id(), "F4:24:00:C8:07:11")


class TLVEOLLDPDUTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_eolldpdu(self):
        tlv = eolldpdu.TVLEoLLDPDU()
        self.assertEqual(tlv.length, 0)
        self.assertEqual(tlv.type, 0)
        self.assertEqual(tlv.value_bytes(), bytearray())
        self.assertEqual(tlv.dump(), b'\x00\x00')
