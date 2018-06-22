import socket
import threading

from PyQt4.QtCore import QThread


class SetterGetterPacketSniff:
    def __init__(self):
        self.IPDevice = None
        self.dicIPHostName = {}
        self.dicCounterRequest = {}
        self.dicTimeForPerRequest = {}
        self.dicLengthData = {}
        # header packet
        self.packetStruct = None
        self.ethAdderSourceMAC = None
        self.ethAdderDestinationMAC = None
        self.protocol = None
        self.Ip_Header_Version = None
        self.Ip_Header_IPHeaderLength = None
        self.Ip_Header_TTL = None
        self.Ip_Header_SourceAddress = None
        self.Ip_Header_DestinationAddress = None
        # tcp
        self.TCP_Protocol_SourcePort = None
        self.TCP_Protocol_DestinationPort = None
        self.TCP_Protocol_SequenceNumber = None
        self.TCP_Protocol_Acknowledgement = None
        self.TCP_Protocol_TCPHeaderLength = None
        # icmp
        self.ICMP_Packets_Type = None
        self.ICMP_Packets_Code = None
        self.ICMP_Packets_Checksum = None
        # udp
        self.UDP_packets_Source_Port = None
        self.UDP_packets_Destination_Port = None
        self.UDP_packets_Length = None
        self.UDP_packets_Checksum = None
        # end udp
        self.Checked_Protocol = None
        self.data = None
        self.timeOFGeneratePacket = None
        self.packetString = None
        self.lengthData = None

    def generatPacketString(self):
        self.lengthData = len(self.data)
        if self.Checked_Protocol == "TCP":
            self.packetString = \
                'Time : ' + self.timeOFGeneratePacket.__str__() + "\n" \
                + 'Source MAC : ' + self.ethAdderSourceMAC.__str__() + "\n" \
                + 'Destination MAC : ' + self.ethAdderDestinationMAC.__str__() + "\n" \
                + 'Protocol : ' + self.protocol.__str__() + "\n" \
                + 'Version : ' + self.Ip_Header_Version.__str__() + "\n" \
                + 'IP Header Length : ' + self.Ip_Header_IPHeaderLength.__str__() + "\n" \
                + 'TTL : ' + self.Ip_Header_TTL.__str__() + "\n" \
                + 'Source Address : ' + self.Ip_Header_SourceAddress.__str__() + "\n" \
                + 'Destination Address : ' + self.Ip_Header_DestinationAddress.__str__() + "\n" \
                + 'Protocol : ' + self.Checked_Protocol.__str__() + "\n" \
                + 'Source Port : ' + self.TCP_Protocol_SourcePort.__str__() + "\n" \
                + 'Dest Port : ' + self.TCP_Protocol_DestinationPort.__str__() + "\n" \
                + 'Sequence Number : ' + self.TCP_Protocol_SequenceNumber.__str__() + "\n" \
                + 'Acknowledgement : ' + self.TCP_Protocol_Acknowledgement.__str__() + "\n" \
                + 'TCP header length : ' + self.TCP_Protocol_TCPHeaderLength.__str__() + "\n"
        elif self.Checked_Protocol == "UDP":
            self.packetString = \
                'Time : ' + self.timeOFGeneratePacket.__str__() + "\n" \
                + 'Source MAC : ' + self.ethAdderSourceMAC.__str__() + "\n" \
                + 'Destination MAC : ' + self.ethAdderDestinationMAC.__str__() + "\n" \
                + 'Protocol : ' + self.protocol.__str__() + "\n" \
                + 'Version : ' + self.Ip_Header_Version.__str__() + "\n" \
                + 'IP Header Length : ' + self.Ip_Header_IPHeaderLength.__str__() + "\n" \
                + 'TTL : ' + self.Ip_Header_TTL.__str__() + "\n" \
                + 'Source Address : ' + self.Ip_Header_SourceAddress.__str__() + "\n" \
                + 'Destination Address : ' + self.Ip_Header_DestinationAddress.__str__() + "\n" \
                + 'Protocol : ' + self.Checked_Protocol.__str__() + "\n" \
                + 'Type : ' + self.ICMP_Packets_Type.__str__() + "\n" \
                + 'Code : ' + self.ICMP_Packets_Code.__str__() + "\n" \
                + 'Checksum : ' + self.ICMP_Packets_Checksum.__str__() + "\n"

        elif self.Checked_Protocol == "ICMP":
            self.packetString = \
                'Time : ' + self.timeOFGeneratePacket.__str__() + "\n" \
                + 'Source MAC : ' + self.ethAdderSourceMAC.__str__() + "\n" \
                + 'Destination MAC : ' + self.ethAdderDestinationMAC.__str__() + "\n" \
                + 'Protocol : ' + self.protocol.__str__() + "\n" \
                + 'Version : ' + self.Ip_Header_Version.__str__() + "\n" \
                + 'IP Header Length : ' + self.Ip_Header_IPHeaderLength.__str__() + "\n" \
                + 'TTL : ' + self.Ip_Header_TTL.__str__() + "\n" \
                + 'Source Address : ' + self.Ip_Header_SourceAddress.__str__() + "\n" \
                + 'Destination Address : ' + self.Ip_Header_DestinationAddress.__str__() + "\n" \
                + 'Protocol : ' + self.Checked_Protocol.__str__() + "\n" \
                + 'Source Port : ' + self.UDP_packets_Source_Port.__str__() + "\n" \
                + 'Dest Port : ' + self.UDP_packets_Destination_Port.__str__() + "\n" \
                + 'Length : ' + self.UDP_packets_Length.__str__() + "\n" \
                + 'Checksum : ' + self.UDP_packets_Checksum.__str__() + "\n"
        self.packetString += "length Data: " + self.lengthData.__str__() + "\n" + "Data: " + self.data.__str__() + "\n"

    def getSubnetMaskANDIPRnage(self):
        ip = self.IPDevice.split(".")
        self.IPDevice = ip  # [192,168,1,1]
        # string = subprocess.call(['dir'])

    def setCounterSourceIp(self):
        ip = self.Ip_Header_SourceAddress.split(".")
        if self.IPDevice[0] == ip[0] and self.IPDevice[1] == ip[1] and self.IPDevice[2] == ip[2]:
            # if self.Ip_Header_SourceAddress.__str__()
            if self.dicCounterRequest.has_key(self.Ip_Header_SourceAddress.__str__()):

                self.dicCounterRequest[self.Ip_Header_SourceAddress.__str__()].append(
                    self.dicCounterRequest[self.Ip_Header_SourceAddress.__str__()].__len__())

                self.dicTimeForPerRequest[self.Ip_Header_SourceAddress.__str__()].append(self.timeOFGeneratePacket)
                self.dicLengthData[self.Ip_Header_SourceAddress.__str__()].append(self.lengthData)
                # T = threading.Thread(self.getHostNameBYIP())
                # T.start()
                # T.join()
                # print self.Ip_Header_SourceAddress, self.dicCounterRequest[self.Ip_Header_SourceAddress.__str__()]
                # print self.dicCounterRequest
            else:
                self.dicCounterRequest[self.Ip_Header_SourceAddress.__str__()] = [0, 1]
                self.dicTimeForPerRequest[self.Ip_Header_SourceAddress.__str__()] = [0, self.timeOFGeneratePacket]
                self.dicLengthData[self.Ip_Header_SourceAddress.__str__()] = [0, self.lengthData.__str__()]

                T1 = threading.Thread(self.getHostNameBYIP())
                T1.start()

                # print self.dicTimeForPerRequest[self.Ip_Header_SourceAddress.__str__()].__len__(), self.dicCounterRequest[
                #     self.Ip_Header_SourceAddress.__str__()].__len__(),self.dicLengthData[self.Ip_Header_SourceAddress.__str__()].__len__()
        else:
            pass

    def getHostNameBYIP(self):
        # T1 = threading.Thread(list(socket.gethostbyaddr(self.Ip_Header_SourceAddress.__str__())))
        # T1.start()
        string = list(socket.gethostbyaddr(self.Ip_Header_SourceAddress.__str__()))
        print string
        self.dicIPHostName[self.Ip_Header_SourceAddress] = string[0]

