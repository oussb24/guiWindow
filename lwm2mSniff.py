
from marshal import dumps
import pyshark


import scapy
from telnetlib import IP, TLS
from scapy.all import *
import scapy 

from PyQt5.QtCore import pyqtSignal
packetLen_global =  ""
packet_number= ""
class lwm2mSniffer(object):
    newPacketSignal = pyqtSignal()    

    packet_dict = {}
    DTLS_packet = ""
    lwm2m_appData_Len =  ""
    packetLen= ""
    totalLen = ""
    packet_number_int=0
    def __init__(self):
        self.packetToJson()
        threading.Thread(target=self.saveTofile)
    def packetToJson(self):
        global packetLen_global,packet_number
        capture = pyshark.LiveCapture(interface="Ethernet 2",bpf_filter='udp port 5684')
        
        for packet in capture.sniff_continuously():
                self.packet_number_int = self.packet_number_int +1
                #self.totalLen= self.totalLen + packet.length
                #print(vars(packet.layers[3]._all_fields))
                #dtls_record_proto = packet.layers[3]
                #dtls_record = str(packet.layers[3]._all_fields['dtls.record'])
                self.DTLS_record = packet.layers[3]._all_fields['dtls.record']  #"DTLSv1.2 Record Layer: Application Data Protocol: coap"  , 
                # if "coap" in self.DTLS_record:
                #     self.lwm2m_appData_Len = packet.length
                #     packetLen_global =  "lwm2m packet "+ str(self.lwm2m_appData_Len) +'\n' + packetLen_global
                # else:
                #     self.DTLS_packet =  packet.length
                  
                # packetLen_global =  "dtls packet " + str(self.DTLS_packet) +'\n' + packetLen_global    
                packetLen_global = packet.length +'\n' + packetLen_global  
                packet_number = str(self.packet_number_int)+'\n'
                
    def saveTofile(self):
        pyshark.FileCapture('C:\\Users\\GFWN4976\\Documents\\Stage\\DemoLwm2m\\qtGUI\\clean\\window\\lwm2mDemo\\file.pcap',display_filter="udp port 5684")
                


#lw = lwm2mSniffer()