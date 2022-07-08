
from marshal import dumps
import pyshark


import scapy
from telnetlib import IP, TLS
from scapy.all import *
import scapy 

from PyQt5.QtCore import pyqtSignal
packetLen_global =  ""
class lwm2mSniffer(object):
    newPacketSignal = pyqtSignal()    

    packet_dict = {}
    DTLS_record = ""   
    packetLen= ""
    totalLen = ""
    
    def __init__(self):
        self.packetToJson()
    def packetToJson(self):
        global packetLen_global
        capture = pyshark.LiveCapture(interface="Ethernet 2",bpf_filter='udp port 5684')
        for packet in capture.sniff_continuously():
                #self.totalLen= self.totalLen + packet.length
                #print(vars(packet.layers[3]._all_fields))
                #dtls_record_proto = packet.layers[3]
                #dtls_record = str(packet.layers[3]._all_fields['dtls.record'])
                self.DTLS_record = packet.layers[3]._all_fields['dtls.record']  #"DTLSv1.2 Record Layer: Application Data Protocol: coap"  , 
                #print(self.DTLS_record)
                self.packetLen =  packet.length
                packetLen_global =  str(packet.length) +'\n' + packetLen_global  
  

