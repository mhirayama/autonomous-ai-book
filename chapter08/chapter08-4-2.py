import socket


RASPBERRY_PI_IP = "192.168.128.152"
PORT = 5000


message = "hello"


sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.connect(
    (RASPBERRY_PI_IP, PORT)
)

sock.sendall(
    message.encode("utf-8")
)

sock.close()

print("メッセージを送信しました")
