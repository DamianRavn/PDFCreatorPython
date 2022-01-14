from Packet import Packet
import socket
import threading
import ServerHandler

PORT = 5050
SERVER = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())


def send_data(client_socket: socket, data: Packet) -> None:
    data.write_length_of_packet()
    client_socket.send(data.buffer)


def client_handler(client_socket: socket, address: str) -> None:
    print(f"[NEW CONNECTION] {address} connected")

    while True:
        data_packet_size = client_socket.recv(4)
        if not data_packet_size:
            print("[NO DATA RECIEVED] Server didn't recieve any data, closing socket")
            break

        data_size = int.from_bytes(data_packet_size, "little", signed=True)
        rest_of_data_packet = client_socket.recv(data_size)
        ServerHandler.handle_data(rest_of_data_packet)

    client_socket.close()


def start():
    server.listen(1)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket, address))
        client_thread.daemon = True  # Daemon threads are abruptly stopped at shutdown.
        client_thread.start()
        send_data(client_socket, ServerHandler.send_welcome_client("Welcome to the Python Server!"))
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

print("[STARTING] server is starting")
start()
