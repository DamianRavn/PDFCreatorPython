import PDFCreator
import Packet
from sys import exc_info

#Send data
def SendWelcomeClient(stringmsg: str) -> Packet.Packet:
    packet = Packet.Packet(0)
    packet.WriteInt(int(Packet.ServerPackets.welcome))
    packet.WriteString(stringmsg)
    packet.WriteInt(0)
    return packet

#Recieve data
def WelcomeReceived(packet:Packet.Packet) -> None:
    clientIdCheck = packet.ReadInt()
    username = packet.ReadString()
    print(f"{username} connected with clientId: {clientIdCheck}")


def MakeNewDocument(packet:Packet.Packet) -> None:
    print(f"[MAKING DOCUMENT]")


def ImageReceived(packet:Packet.Packet) -> None:
    print(f"[PLACING IMAGE]")

def RTFTextWithTagsReceived(packet:Packet.Packet) -> None:
    print(f"[PARSING RTF TEXT]")

def SaveDocument(packet:Packet.Packet) -> None:
    print(f"[SAVING DOCUMENT]")

def Disconnect(packet:Packet.Packet) -> None:
    print(f"[DISCONNECTED]")

ENUMTOFUNCDIC = {int(Packet.ClientPackets.welcomeReceived) : WelcomeReceived, int(Packet.ClientPackets.image) : ImageReceived, int(Packet.ClientPackets.RTFTextWithTags) : RTFTextWithTagsReceived, int(Packet.ClientPackets.makeDocument) : MakeNewDocument, int(Packet.ClientPackets.saveDocument) : SaveDocument, int(Packet.ClientPackets.disconnect) : Disconnect}

def handle_data(dataToHandle) -> None:
    try:
        packet = Packet.Packet(dataToHandle)
        functionCall = packet.ReadInt()
        ENUMTOFUNCDIC[functionCall](packet)
    except:
        print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")
    
