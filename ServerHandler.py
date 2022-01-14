import PDFCreator
import Packet
import PDFCreator
from sys import exc_info


# Send data
def send_welcome_client(string_msg: str) -> Packet.Packet:
    packet = Packet.Packet(0)
    packet.write_int(int(Packet.ServerPackets.welcome))
    packet.write_string(string_msg)
    packet.write_int(0)
    return packet


# Recieve data
def welcome_received(packet: Packet.Packet) -> None:
    client_id_check = packet.read_int()
    username = packet.read_string()
    print(f"{username} connected with clientId: {client_id_check}")


def make_new_document(packet: Packet.Packet) -> None:
    print(f"[MAKING DOCUMENT]")
    name = packet.read_string()
    amountOfPages = packet.read_int()
    width = packet.read_float()
    height = packet.read_float()
    PDFCreator.create_document(name, amountOfPages, width, height)


def image_received(packet: Packet.Packet) -> None:
    print(f"[PLACING IMAGE]")
    documentName = packet.read_string()
    path = packet.read_string()
    pageNR = packet.read_int()
    pivotX = packet.read_float()
    pivotY = packet.read_float()
    sizeX = packet.read_float()
    sizeY = packet.read_float()
    posX = packet.read_float()
    posY = packet.read_float()

    PDFCreator.draw_image(documentName, path, pageNR, pivotX, pivotY, sizeX, sizeY, posX, posY)


def rtf_text_with_tags_received(packet: Packet.Packet) -> None:
    print(f"[PARSING RTF TEXT]")
    documentName = packet.read_string()
    RTFtext = packet.read_string()
    pageNR = packet.read_int()
    fontFamily = packet.read_string()
    fontSize = packet.read_float()
    fontStyle = packet.read_int()
    alignment = packet.read_int()
    lineSpace = packet.read_float()
    paragraphSpace = packet.read_float()
    pivotX = packet.read_float()
    pivotY = packet.read_float()
    sizeX = packet.read_float()
    sizeY = packet.read_float()
    posX = packet.read_float()
    posY = packet.read_float()

    PDFCreator.draw_RTF_string(documentName, RTFtext, pageNR, fontFamily, fontSize, fontStyle, alignment,
                                           lineSpace, paragraphSpace, pivotX, pivotY, sizeX, sizeY, posX, posY)


def save_document(packet: Packet.Packet) -> None:
    print(f"[SAVING DOCUMENT]")
    path = packet.read_string()
    name = packet.read_string()
    PDFCreator.save_document()


def disconnect(packet: Packet.Packet) -> None:
    print(f"[DISCONNECTED]")


ENUMTOFUNCDIC = {int(Packet.ClientPackets.welcomeReceived): welcome_received,
                 int(Packet.ClientPackets.image): image_received,
                 int(Packet.ClientPackets.RTFTextWithTags): rtf_text_with_tags_received,
                 int(Packet.ClientPackets.makeDocument): make_new_document,
                 int(Packet.ClientPackets.saveDocument): save_document, int(Packet.ClientPackets.disconnect): disconnect}


def handle_data(data_to_handle) -> None:
    try:
        packet = Packet.Packet(data_to_handle)
        function_call = packet.read_int()
        ENUMTOFUNCDIC[function_call](packet)
    except:
        print(f"[Error] exception msg: {exc_info()}, traceback: {(exc_info()[2]).tb_frame}")
