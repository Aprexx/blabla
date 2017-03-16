import argparse
import threading
from lldpa.lldpAgent import LLDPAgent

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='LLDP Agent.')
    parser.add_argument('-i', metavar='interface', default="eth0", type=str, nargs='?',
                        help='name of the interface the agents binds to')
    parser.add_argument('-s', action="store_false")
    parser.add_argument('-m', metavar='sets the source mac', default=None, type=str,
                        nargs='?', help='Set the source mac for testing purpose')

    args = parser.parse_args()
    a = LLDPAgent(interface_name=args.i, src_mac=args.m)
    if args.s:
        t = threading.Thread(target=a.run_announce)
        t.daemon = True
        t.start()

    a.run_receive()
