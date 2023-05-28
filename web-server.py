from socket import *
import os

HOST = '127.0.0.1'  # Mendefinisikan alamat IP lokal untuk server (localhost)
PORT = 8080  # Mendefinisikan nomor port untuk server


# Membuat objek socket dengan menggunakan alamat IP versi 4 dan protokol TCP
server_socket = socket(AF_INET, SOCK_STREAM)
# Mengikat socket ke alamat IP dan port yang telah ditentukan
server_socket.bind((HOST, PORT))
# Mengizinkan socket untuk menerima koneksi dari client dengan jumlah maksimum koneksi yang diterima adalah 1
server_socket.listen(1)
# Mencetak pesan untuk menampilkan alamat dan port server yang sedang berjalan
print(f"Server berjalan di http://{HOST}:{PORT}")

while True:
    # Menerima koneksi dari client dan mengembalikan objek socket baru (client_socket) dan alamat client (client_address)
    client_socket, client_address = server_socket.accept()
    print(f"Koneksi diterima dari {client_address}")
    # Menerima data dari client (request) dengan ukuran buffer maksimum 1024 byte dan mengubahnya ke dalam bentuk string.
    request = client_socket.recv(1024).decode()
    print(f"Request:\n{request}")
    # Memecah string request menjadi bagian-bagian yang terpisah menggunakan spasi sebagai pemisah dan menyimpannya dalam list (request_parts)
    request_parts = request.split()
    # Mengambil metode HTTP (GET, POST, dll.) dari request
    method = request_parts[0]
    # Mengambil path file yang diminta oleh client dari request dan menghilangkan leading slash '/'
    file_path = request_parts[1][1:]
    if file_path == '':
        file_path = 'index.html'
    if method == 'GET':  # Memeriksa jika metode yang digunakan adalah GET
        # Memeriksa jika file yang diminta oleh client ada pada server menggunakan fungsi os.path.exists()
        if os.path.exists(file_path):
            # Membuka file yang diminta dalam mode read ('r') dan menyimpannya dalam objek file
            with open(file_path, 'r') as file:
                # Membuat response message dengan status code 200 OK dan memasukkan konten file yang diminta ke dalamnya
                response = f"HTTP/1.1 200 OK\n\n{file.read()}"
        else:
            # Membuat response message dengan status code 404 Not Found karena file yang diminta tidak ditemukan
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found"
    else:
        # Membuat response message dengan status code 405 Method Not Allowed karena metode yang digunakan oleh client tidak diizinkan
        response = "HTTP/1.1 405 Method Not Allowed\n\n405 Method Not Allowed"
    # Mengirimkan response message ke client dalam bentuk byte setelah dienkripsi menggunakan metode encode()
    client_socket.sendall(response.encode())
    # Menutup koneksi dengan client.
    client_socket.close()
