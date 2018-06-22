from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import socket
from struct import *
import time
from PyQt4 import QtCore
import pcapy
import sys
import timer


class LocalSniffer(QtCore.QObject):
    ObjectUpdated = QtCore.pyqtSignal([object], [unicode])

    def __init__(self):
        super(self.__class__, self).__init__()
        self.choiceDevice = None
        from interface_sniff.SetterGetterPacketSniff import SetterGetterPacketSniff

        self.setterGetterPacketSniff = SetterGetterPacketSniff()

    def initializObject(self):
        # list all devices
        return pcapy.findalldevs()
        # print devices
        # ask user to enter device name to sniff
        # print "Available devices are :"
        # for d in devices:
        #     # print(d)
        #     yield d
        # return devices

    def main(self, argv):
        # dev = raw_input("Enter device name to sniff : ")
        dev = self.choiceDevice.__str__()
        # print "Sniffing device " + dev

        '''
        open device
        # Arguments here are:
        #   device
        #   snaplen (maximum number of bytes to capture _per_packet_)
        #   promiscious mode (1 for true)
        #   timeout (in milliseconds)
        '''
        cap = pcapy.open_live(dev, 65536, 1, 0)

        # start sniffing packets

        try:
            while 1:
                (header, packet) = cap.next()
                # print (
                #     "{0:s}: captured {1:d} bytes, truncated to {2:d} bytes".format(datetime.datetime.now(), header.getlen(),
                #                                                                    header.getcaplen()))
                self.setterGetterPacketSniff.timeOFGeneratePacket = millis = int(round(time.time() * 1000))
                try:
                    self.parse_packet(packet)
                    self.ObjectUpdated.emit(self.setterGetterPacketSniff)
                except:
                    print("the application throws Exception in down layer ! :( ")
        except:
            print("be khater hajm balaye darkhast tavanii pardaszesh nadaram :( ")

    # Convert a string of 6 characters of ethernet address into a dash separated hex string

    def eth_addr(self, a):
        b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]), ord(a[1]), ord(a[2]), ord(a[3]), ord(a[4]), ord(a[5]))
        return b

    # function to parse a packet
    def parse_packet(self, packet):
        # parse ethernet header
        eth_length = 14
        eth_header = packet[:eth_length]
        eth = unpack('!6s6sH', eth_header)
        eth_protocol = socket.ntohs(eth[2])
        # print 'Destination MAC : ' + self.eth_addr(packet[0:6]) + ' Source MAC : ' + self.eth_addr(
        #     packet[6:12]) + ' Protocol : ' + str(eth_protocol)

        # Parse IP packets, IP Protocol number = 8
        if eth_protocol == 8:
            # Parse IP header
            # take first 20 characters for the ip header
            ip_header = packet[eth_length:20 + eth_length]

            # now unpack them :)
            iph = unpack('!BBHHHBBH4s4s', ip_header)

            version_ihl = iph[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF

            iph_length = ihl * 4

            ttl = iph[5]
            protocol = iph[6]
            s_addr = socket.inet_ntoa(iph[8])
            d_addr = socket.inet_ntoa(iph[9])
            self.setterGetterPacketSniff.ethAdderDestinationMAC = self.eth_addr(packet[0:6])
            self.setterGetterPacketSniff.ethAdderSourceMAC = self.eth_addr(packet[6:12])
            self.setterGetterPacketSniff.protocol = str(eth_protocol)
            self.setterGetterPacketSniff.Ip_Header_Version = str(version)
            self.setterGetterPacketSniff.Ip_Header_IPHeaderLength = str(ihl)
            self.setterGetterPacketSniff.Ip_Header_TTL = str(ttl)
            self.setterGetterPacketSniff.Ip_Header_SourceAddress = str(s_addr)
            self.setterGetterPacketSniff.Ip_Header_DestinationAddress = str(d_addr)
            # self.setterGetterPacketSniff.Ip_Header_Protocol_2 = str(protocol)
            # print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(
            #     ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(
            #     s_addr) + ' Destination Address : ' + str(d_addr)

            # TCP protocol
            if protocol == 6:
                t = iph_length + eth_length
                tcp_header = packet[t:t + 20]

                # now unpack them :)
                tcph = unpack('!HHLLBBHHH', tcp_header)

                source_port = tcph[0]
                dest_port = tcph[1]
                sequence = tcph[2]
                acknowledgement = tcph[3]
                doff_reserved = tcph[4]
                tcph_length = doff_reserved >> 4
                self.setterGetterPacketSniff.Checked_Protocol = "TCP"
                self.setterGetterPacketSniff.TCP_Protocol_SourcePort = str(source_port)
                self.setterGetterPacketSniff.TCP_Protocol_DestinationPort = str(dest_port)
                self.setterGetterPacketSniff.TCP_Protocol_SequenceNumber = str(sequence)
                self.setterGetterPacketSniff.TCP_Protocol_Acknowledgement = str(acknowledgement)
                self.setterGetterPacketSniff.TCP_Protocol_TCPHeaderLength = str(tcph_length)
                # print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(
                #     dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(
                #     acknowledgement) + ' TCP header length : ' + str(tcph_length)

                h_size = eth_length + iph_length + tcph_length * 4
                data_size = len(packet) - h_size

                # get data from the packet
                data = packet[h_size:]
                self.setterGetterPacketSniff.data = data
                # print 'Data : ' + data

            # ICMP Packets
            elif protocol == 1:
                u = iph_length + eth_length
                icmph_length = 4
                icmp_header = packet[u:u + 4]

                # now unpack them :)
                icmph = unpack('!BBH', icmp_header)

                icmp_type = icmph[0]
                code = icmph[1]
                checksum = icmph[2]
                self.setterGetterPacketSniff.Checked_Protocol = "ICMP"
                self.setterGetterPacketSniff.ICMP_Packets_Type = str(icmp_type)
                self.setterGetterPacketSniff.ICMP_Packets_Code = str(code)
                self.setterGetterPacketSniff.ICMP_Packets_Checksum = str(checksum)
                # print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)

                h_size = eth_length + iph_length + icmph_length
                data_size = len(packet) - h_size

                # get data from the packet
                data = packet[h_size:]
                self.setterGetterPacketSniff.data = data
                # print 'Data : ' + data

            # UDP packets
            elif protocol == 17:
                u = iph_length + eth_length
                udph_length = 8
                udp_header = packet[u:u + 8]

                # now unpack them :)
                udph = unpack('!HHHH', udp_header)

                source_port = udph[0]
                dest_port = udph[1]
                length = udph[2]
                checksum = udph[3]
                self.setterGetterPacketSniff.Checked_Protocol = "UDP"
                self.setterGetterPacketSniff.UDP_packets_Source_Port = str(source_port)
                self.setterGetterPacketSniff.UDP_packets_Destination_Port = str(dest_port)
                self.setterGetterPacketSniff.UDP_packets_Length = str(length)
                self.setterGetterPacketSniff.UDP_packets_Checksum = str(checksum)
                # print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(
                #     length) + ' Checksum : ' + str(checksum)

                h_size = eth_length + iph_length + udph_length
                data_size = len(packet) - h_size

                # get data from the packet
                data = packet[h_size:]
                self.setterGetterPacketSniff.data = data
                # print 'Data : ' + data

            # some other IP packet like IGMP
            else:
                self.setterGetterPacketSniff.Checked_Protocol = "IGMP or Other"
                print('Protocol other than TCP/UDP/ICMP \n ')

        elif eth_protocol == 1544:
            pass
            # self.setterGetterPacketSniff.Checked_Protocol = "IGMP or Other"
            # print 'Protocol other than TCP/UDP/ICMP'
