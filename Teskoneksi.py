import socket
import time

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.10.112', 12345)  # Sesuaikan dengan alamat IP server dan port
    while True:
        try:
            client_socket.connect(server_address)
            print("Terhubung ke server.")
            return client_socket
        except (ConnectionError, TimeoutError) as e:
            print("Gagal terhubung ke server:", e)
            print("Akan mencoba lagi dalam beberapa detik...")
            time.sleep(5)  # Menunggu beberapa detik sebelum mencoba lagi

# Fungsi untuk mengirim pesan ping ke server
def send_ping(client_socket):
    try:
        # Pengujian koneksi sebelum mengirim pesan
        if client_socket.fileno() == -1:
            # Jika koneksi telah ditutup, coba buat koneksi baru
            print("Koneksi ditutup. Mencoba menyambung kembali ke server...")
            client_socket = connect_to_server()  # Update socket yang digunakan
            if client_socket:
                print("Koneksi berhasil dibuat kembali.")
        else:
            client_socket.sendall("Ping".encode())
            print("Pesan ping terkirim")
    except OSError as e:
        if e.errno == 10054:  # WinError 10054: An existing connection was forcibly closed by the remote host
            print("Koneksi terputus oleh server. Mencoba menyambung kembali...")
            client_socket.close()
            client_socket = connect_to_server()  # Mencoba menyambung kembali ke server
            if client_socket:
                print("Terhubung kembali ke server.")
        else:
            print("Gagal mengirim pesan:", e)
    except Exception as e:
        print("Gagal mengirim pesan:", e)
    return client_socket  # Kembalikan socket yang baru atau yang telah diperbarui

# Inisialisasi socket dan koneksi ke server
client_socket = connect_to_server()

# Loop utama
while True:
    try:
        # Kirim pesan ping ke server
        client_socket = send_ping(client_socket)  # Perbarui socket jika diperlukan
        
        # Tunggu 5 detik sebelum mengirim pesan ping lagi
        time.sleep(5)
    
    except (ConnectionResetError, BrokenPipeError):
        print("Koneksi ke server terputus. Akan mencoba menyambung kembali...")
        client_socket.close()
        while True:
            try:
                client_socket = connect_to_server()  # Mencoba menyambung kembali ke server
                print("Terhubung kembali ke server.")
                # Setelah tersambung kembali, loop utama akan melanjutkan pengiriman pesan ping
                break  
            except (ConnectionError, TimeoutError):
                print("Gagal menyambung kembali ke server. Akan mencoba lagi dalam beberapa detik...")
                time.sleep(5)
