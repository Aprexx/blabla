import unittest
import binascii
import os
import platform
import socket
import subprocess
import sys
import threading
import time
from lldpa.lldpAgent import LLDPAgent
from lldpa.lldpMessage import LLDPMessage


class LLDPAgentTests(unittest.TestCase):
    def setUp(self):
        self.os = platform.system()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.file_path = os.path.join(dir_path[:-5], "main.py")
        self.python_executable = sys.executable

    def test_send(self):
        a = LLDPAgent("eth0", send_interval_sec=1)
        a.src_ip_address = '127.0.0.1'
        a.src_mac = '\x01\x23\x45\x67\x89\xab'
        recv_socket = None

        t = threading.Thread(target=a.run_announce)
        t.daemon = True
        t.start()

        time.sleep(1)

        recv_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        recv_socket.bind((a.interface_name, 0))

        while True:
            data = recv_socket.recv(4096)

            if data[12:14] == '\x88\xcc':
                break

        self.assertEqual(data[0:6], '\x01\x80\xc2\x00\x00\x0e')
        self.assertEqual(a.src_mac, data[6:12])
        self.assertEqual(data[12:14], '\x88\xcc')
        message = LLDPMessage("01:23:45:67:89:AB")
        message.load(data[14:])

        self.assertEqual(message.__str__(), "LLDPMessage(src_mac=01:23:45:67:89:AB,chassis_id=01:23:45:67:89:AB,"
                                            "port_id=01:23:45:67:89:AB,ttl=120)")

        recv_socket.close()
        a.stop()

    def test_receive(self):
        sending_socket = None
        execute_list = ["sudo", self.python_executable, self.file_path, '-s', '-i', 'eth0', '-m', '01:23:45:67:89:ab']
        p = subprocess.Popen(execute_list, shell=False, stdout=subprocess.PIPE)

        time.sleep(1)

        sending_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        sending_socket.bind(("eth0", 0))

        full_msg = '0180c200000e0123456789ad88cc0207040123456789ab0407030123456789ab060200780000'

        sending_socket.send(binascii.unhexlify(full_msg))

        sending_socket.close()

        printed_message = ""
        while True:
            next_line = p.stdout.readline()
            if next_line == '':
                break
            if next_line[0:11] == "LLDPMessage":
                printed_message = next_line
                break
            sys.stdout.write(next_line)
            sys.stdout.flush()

        self.assertEqual(printed_message, "LLDPMessage(src_mac=01:23:45:67:89:AD,chassis_id=01:23:45:67:89:AB,"
                                          "port_id=01:23:45:67:89:AB,ttl=120)\n")

    def test_ignore_own_messages(self):
        sending_socket = None
        execute_list = ["sudo", self.python_executable, self.file_path, '-s', '-i', 'eth0', '-m', '01:23:45:67:89:ab']
        p = subprocess.Popen(execute_list, shell=False, stdout=subprocess.PIPE)
        time.sleep(1)

        sending_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        sending_socket.bind(('eth0', 0))

        full_msg = '0180c200000e0123456789ab88cc0207040123456789ab0407030123456789ab060200780000'

        sending_socket.send(binascii.unhexlify(full_msg))

        sending_socket.close()

        printed_message = None
        while True:
            next_line = p.stdout.readline()
            if next_line == '':
                break
            if next_line == 'Ignoring own message\n':
                printed_message = ""
                break
            sys.stdout.write(next_line)
            sys.stdout.flush()
        self.assertEqual(printed_message, "")
