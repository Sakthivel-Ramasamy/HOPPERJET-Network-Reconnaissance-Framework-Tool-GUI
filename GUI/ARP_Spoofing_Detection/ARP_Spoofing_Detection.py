import datetime
import json
import nmap
import os
from scapy.all import *
import sys

#Start of Get Current Time Function

def gettime():
    try:
        current_time=datetime.datetime.now()
    except Exception:
        current_time=datetime.now()
    return current_time

#End of Get Current Time Function

#Start of ARP Spoofing Detection Scanner

def arp_spoof_safe():
    arp_spoofing_detection_scanner_stop_time=gettime()
    output=open(os.path.dirname(__file__)+"/../output.hop", "a")
    output.truncate(0)
    output.write("ARP Spoofing Detection Scan started at {}".format(arp_spoofing_detection_scanner_start_time))
    output.write("\n\nTimestamp: {}\nMessage: You are safe".format(gettime()))
    output.write("\n\nARP Spoofing Detection Scanner ended at {}".format(arp_spoofing_detection_scanner_stop_time))
    output.write("\nTotal Scan Duration in Seconds = {}".format(abs(arp_spoofing_detection_scanner_stop_time-arp_spoofing_detection_scanner_start_time).total_seconds()))
    output.close()
    exit_process()

def arp_spoof_not_safe(a):
    arp_spoofing_detection_scanner_stop_time=gettime()
    output=open(os.path.dirname(__file__)+"/../output.hop", "a")
    output.truncate(0)
    output.write("ARP Spoofing Detection Scan started at {}".format(arp_spoofing_detection_scanner_start_time))
    output.write("\n\nTimestamp: {}\nMessage: You are under attack\nVictim's MAC Address: {}\nAttacker's MAC Address: {}".format(gettime(), a[0], a[1]))
    output.write("\n\nARP Spoofing Detection Scanner ended at {}".format(arp_spoofing_detection_scanner_stop_time))
    output.write("\nTotal Scan Duration in Seconds = {}".format(abs(arp_spoofing_detection_scanner_stop_time-arp_spoofing_detection_scanner_start_time).total_seconds()))
    output.close()
    attack_output=open(os.path.dirname(__file__)+"/../error.hop", "w")
    attack_output.close()
    exit_process()

#Function to get MAC Addrees by broadcasting the ARP message packets 
def arp_spoof_mac_identifier(ip):
    p = Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip) 
    result = srp(p, timeout=3, verbose=False)[0] 
    return result[0][1].hwsrc

#Function to process every packet received by sniff function 
def arp_spoof_identifier(packet):
    global arpcount, arp_spoofing_detection_scanner_start_time
    if packet.haslayer(ARP) and packet[ARP].op == 2: 
        a=[]	 
        try: 
            #Get the sender's real MAC Address 
            real_mac = arp_spoof_mac_identifier(packet[ARP].psrc)
            #Get the MAC Address from the packet sent to us 
            response_mac = packet[ARP].hwsrc
            #If both MAC Addresses are different, attack took place
            if real_mac != response_mac: 
                a.append(real_mac) 
                a.append(response_mac)  
                return arp_spoof_not_safe(a) 
            else: 
                arpcount=arpcount+1 
            if arpcount == 40:
                arpcount=0
                return arp_spoof_safe() 
        except IndexError:            	 
            #Error in finding the real MAC Address
            pass

def arp_spoof_detector(interface):
    try:
        sniff(prn=arp_spoof_identifier, iface=interface, store=False)
    except Exception:
        interface=conf.iface
        sniff(prn=arp_spoof_identifier, iface=interface, store=False)

#End of ARP Spoofing Detection Scanner

#Start of Exit Process

def exit_process():
    sys.exit()

#End of Exit Process

#Start of main Function

if __name__=="__main__":

    file=open(os.path.dirname(__file__)+"/../input.json", "r")
    json_data=json.load(file)
    feature=json_data["Method"]
    scan_interface=json_data["Interface"]
    arpcount=0    
    if feature=="ARP Detection":
        arp_spoofing_detection_scanner_start_time=gettime()
        arp_spoof_detector(scan_interface) 
    sys.exit()

#End of main Function