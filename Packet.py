import enum
from sys import exc_info
import struct

#Sent from server to client
class ServerPackets(enum.IntEnum):
    welcome = 1

#Sent from client to server
class ClientPackets(enum.IntEnum):
    welcomeReceived = 1,
    image = 2,
    RTFTextWithTags = 3,
    makeDocument = 5,
    saveDocument = 6,
    disconnect = 7

class structPatterns():
    intPat = "i"
    floatPat = "f"


STRING_FORMAT = "utf-8"
class Packet():

    def __init__(self, databuffer) -> None:
        self.buffer = bytearray(databuffer)
        self.readpos = 0

    #Write section
    # def WriteMultipleValues(self, structPattern : str, *data) -> None:
    #     try:
    #         values = bytearray(struct.calcsize(structPattern))
    #         struct.pack_into(structPattern, values, 0, *data)
    #         self.buffer.extend(values)
    #     except:
    #         print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")

    def WriteLengthOfPacket(self) -> None:
        try:
            value = bytearray(struct.calcsize(structPatterns.intPat))
            struct.pack_into(structPatterns.intPat, value, 0, len(self.buffer))
            self.buffer[0:0] = value
        except:
            print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")

    def WriteInt(self, data : int) -> None:
        try:
            value = bytearray(struct.calcsize(structPatterns.intPat))
            struct.pack_into(structPatterns.intPat, value, 0, data)
            #intBytes = struct.pack("!i", data)
            self.buffer.extend(value)
        except:
            print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")
    
    def WriteFloat(self, data:float) -> None:
        try:
            value = bytearray(struct.calcsize(structPatterns.intPat))
            struct.pack_into(structPatterns.floatPat, value, 0, data)
            self.buffer.extend(value)
            #floatBytes = struct.pack("!f", data)
            #self.buffer.extend(floatBytes)
        except:
            print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")

    def WriteString(self, data : str) -> None:
        try:
            dataSize = len(data)
            self.WriteInt(dataSize)
            self.buffer.extend(data.encode(STRING_FORMAT))
        except:
            print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")
        


    #Read Section
    # def ReadMultipleValues(self, structPattern : str) -> tuple:
    #     try:
    #         size = struct.calcsize(structPattern)
    #         #values = struct.unpack(structPattern, self.buffer[self.readpos : self.readpos + size])
    #         values = struct.unpack_from(structPattern, self.buffer, self.readpos)
    #         self.readpos += size
    #         return values
    #     except:
    #         print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")
            
    def ReadInt(self) -> int:
        try:
            value = struct.unpack_from(structPatterns.intPat, self.buffer, self.readpos)
            #intBytes = self.buffer[self.readpos : self.readpos + 4]
            #value = int.from_bytes(intBytes, byteorder, signed=isSigned)
            self.readpos += struct.calcsize(structPatterns.intPat) 
            return value[0] #unpack returns a tuple even if there's only 1 item
        except:
            print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")

    def ReadFloat(self) -> float:
        try:
            value = struct.unpack_from(structPatterns.floatPat, self.buffer, self.readpos)
            self.readpos += struct.calcsize(structPatterns.floatPat)
            return value[0] #unpack returns a tuple even if there's only 1 item
        except:
            print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")

    def ReadString(self) -> str:
        try:
            stringLength = self.ReadInt()
            string_bytes = self.buffer[self.readpos:self.readpos + stringLength]
            string = string_bytes.decode(STRING_FORMAT)
            self.readpos += stringLength
            return string
        except:
            print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")

# packet = Packet(0)
# packet.WriteInt(3)
# packet.WriteFloat(2.223345456)
# packet.WriteString("Hello1sdadcsd")
# print(packet.ReadInt())
# print(packet.ReadFloat())
# print(packet.ReadString())