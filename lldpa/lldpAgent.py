from __future__ import print_function

import binascii
import platform
import time
import socket
import thread
from lldpa.lldpMessage import LLDPMessage
from lldpa.lldpExceptions import ImproperDestinationMACException


class LLDPAgent:
    def __init__(self, interface_name, port=0, send_interval_sec=10, src_mac=None):
        # Check the OS the application is running on.
        self.os = platform.system()

        self.sending_socket = None
        self.recv_socket = None
        self.interface_name = interface_name
        self.src_mac = self._get_interface_mac(interface_name) if src_mac is None else binascii. \
            unhexlify(src_mac.replace(':', ''))
        self.send_interval_sec = send_interval_sec
        self.terminate = 0
        self.port = port

    def run_receive(self):
        """Agent main loop

        The agent waits for incoming packets to parse them.
        Frames are recognized correctly if the destination MAC matches and the ether_type is 0x88CC.

        :rtype: object
        """

        self.recv_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        self.recv_socket.bind((self.interface_name, self.port))

        while not self.terminate:
            packet = self.recv_socket.recv(65565)
            thread.start_new_thread(self.parse_lldp_frame, (packet,))
            break
        self.recv_socket.close()

    def parse_lldp_frame(self, data):
        """Parser of LLDP frames
        An LLDP Frame is encapsulated in an ethernet frame consisting of destination mac, source mac and ethertype.
        The destination mac has to be valid.
        The ethertype has to be 0x88CC
        LLDP Frame according to IEEE Std 802.1AB-2009:
        http://standards.ieee.org/getieee802/download/802.1AB-2005.pdf

        :param data: the data to parse
        :return:
        """

        temp_type = str(binascii.hexlify(data[12:14]))
        dst = binascii.hexlify((data[0:6]))
        src = binascii.hexlify((data[6:12]))
        print(binascii.hexlify(self.src_mac))
        print(src)
        if binascii.hexlify(self.src_mac) == src:
            print('Ignoring own message\n')
            return
        print(dst)
        if dst == "0180c200000e" or dst == "0180c2000003" or dst == "0180c2000000":
            if temp_type == '88cc':
                lldpM = LLDPMessage()
                lldpM.load(data[14:])
                print(lldpM.__str__())
        else:
            raise ImproperDestinationMACException(dst)


    def run_announce(self):
        """Sends LLDP packets every time interval.

        :return:
        """
        pass  # TODO: Implement raw socket binding.

        while not self.terminate:
            lldpdu = self.generate_lldpdu()
            pass  # TODO: Implement sending. Use the generate_lldpdu() function!
            time.sleep(self.send_interval_sec)

    def generate_lldpdu(self):
        """ Compile an LLDP-DU (data unit) for transmission inside of an ethernet packet.
        Necessary TLVs are:
            - Chassis ID TLV
            - Port ID TLV
            - Time to Live TLV
        """

        # TODO: Implement.
        return bytearray()

    def _get_interface_mac(self, interface_name):
        """Return the MAC address of the given interface.

         This method will try to read the MAC address of the given interface using the /proc filesystem.
         If unsuccessful, will return C{'\\x00\\x00\\x00\\x00\\x00\\x00'}.
         """
        f = None
        try:
            f = open("/sys/class/net/" + interface_name + "/address", 'r')
            mac = f.readline().rstrip()

            return binascii.unhexlify(mac.replace(':', ''))
        except:
            return '\x00' * 6
        finally:
            if f is not None:
                f.close()

    def stop(self):
        """Terminates the running threads"""
        self.terminate = 1
        if self.recv_socket is not None:
            self.recv_socket.close()
