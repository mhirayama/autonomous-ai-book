import socket

HOST = "0.0.0.0"
PORT = 5000


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))

server.listen(1)

print("サーバーを起動しました")
print(f"Port: {PORT}")


while True:

    conn, addr = server.accept()

    print(f"接続: {addr}")

    data = conn.recv(1024)

    if data:

        message = data.decode("utf-8")

        print(f"受信: {message}")

    conn.close()
