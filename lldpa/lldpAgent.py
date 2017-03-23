from __future__ import print_function

import binascii
import platform
import time
import socket

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

        pass  # TODO: Implement raw socket binding.
        self.recv_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.recv_socket.bind('127.0.0.1:'+self.port)


        while not self.terminate:
            pass  # TODO: Implement reception. Use the parse_lldp_frame() function!
            packet = self.recv_socket.recvfrom(65565)
            print(packet)
            self.terminate = 1
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

        # TODO: Implement.

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
