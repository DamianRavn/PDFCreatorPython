from Packet import Packet
import socket
import threading
import ServerHandler

PORT = 5050
SERVER = "127.0.0.1" #socket.gethostbyname(socket.gethostname())

def send_data(clientSocket:socket, data:Packet) -> None:
    data.WriteLengthOfPacket()
    clientSocket.send(data.buffer)
    

def client_handler(clientSocket : socket, address : str) -> None:

    print(f"[NEW CONNECTION] {address} connected")

    while True:
        dataPacketSize = clientSocket.recv(4)
        if not dataPacketSize:
            print("[NO DATA RECIEVED] Server didn't recieve any data, closing socket")
            break

        dataSize = int.from_bytes(dataPacketSize, "little", signed=True)
        restOfDataPacket = clientSocket.recv(dataSize)
        ServerHandler.handle_data(restOfDataPacket)

        
    clientSocket.close()


def start():
    server.listen(1)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        clientSocket, address = server.accept()
        cThread = threading.Thread(target=client_handler, args=(clientSocket, address))
        cThread.daemon = True #Daemon threads are abruptly stopped at shutdown.
        cThread.start()
        send_data(clientSocket, ServerHandler.SendWelcomeClient("Welcome to the Python Server!"))
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

print("[STARTING] server is starting")
start()
