import socket
import os

HOST = 'localhost'
PORT = 8080

# Membuat socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Mengikat socket ke alamat dan port tertentu
server_socket.bind((HOST, PORT))
# Menerima koneksi dari client
server_socket.listen(1)
print(f"Server berjalan di http://{HOST}:{PORT}")

while True:
    # Menerima koneksi dari client
    client_socket, client_address = server_socket.accept()
    print(f"Koneksi diterima dari {client_address}")
    # Menerima request dari client
    request = client_socket.recv(1024).decode()
    print(f"Request:\n{request}")
    # Mem-parse HTTP request
    request_parts = request.split()
    method = request_parts[0]
    file_path = request_parts[1][1:]  # menghilangkan leading slash '/'
    if file_path == '':
        file_path = 'index.html'
    if method == 'GET':
        # Mencari file yang diminta oleh client
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                # Membuat response message dengan header HTTP dan konten file yang diminta
                response = f"HTTP/1.1 200 OK\n\n{file.read()}"
        else:
            # Membuat response message dengan pesan '404 Not Found'
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found"
    else:
        # Membuat response message dengan pesan '405 Method Not Allowed'
        response = "HTTP/1.1 405 Method Not Allowed\n\n405 Method Not Allowed"
    # Mengirimkan response message ke client
    client_socket.sendall(response.encode())
    client_socket.close()
