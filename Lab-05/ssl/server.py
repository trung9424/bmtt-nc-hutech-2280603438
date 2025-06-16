import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

# Danh sách các client đã kết nối
clients = []

def handle_client(client_socket):
    clients.append(client_socket)
    print(f"Đã kết nối với {client_socket.getpeername()}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Nhận dữ liệu: {data.decode('utf-8')}")
            for client in clients:
                if client != client_socket:
                    client.send(data)
    except:
        clients.remove(client_socket)
    finally:
        print(f"Ngắt kết nối với {client_socket.getpeername()}")
        client_socket.close()
        clients.remove(client_socket)

# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

print("Server đang chờ kết nối...")

while True:
    client_socket, client_address = server_socket.accept()

    # Tạo SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=r'M:\bmtt-nc-hutech-2280603438\Lab-05\ssl\certificates\server-cert.crt', 
                            keyfile=r'M:\bmtt-nc-hutech-2280603438\Lab-05\ssl\certificates\server-key.key')
    client_socket = context.wrap_socket(client_socket, server_side=True)

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    