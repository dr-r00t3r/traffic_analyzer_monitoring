import os


class IOStreamMain:
    def __init__(self, listpacket, name=None):
        self.listPacket = None
        self.stringPath = ""
        self.typeFileExtentionToSave = ".txt"
        currentPath = name.rfind(".")
        currentPath = name[:currentPath]

        currentPath = currentPath.split("\\")
        for i in currentPath:
            self.stringPath += i + self.typeFileExtentionToSave
        self.listPacket = listpacket

    def save(self):
        self.fo = open(self.stringPath, 'wb', 2048)
        for i in self.listPacket:
            self.fo.writelines(i.packetString)
        self.fo.close()

    def check(self):
        if not os.path.isdir(self.stringPath):
            return True
        if not os.path.isfile(self.stringPath):
            return True
        return False
