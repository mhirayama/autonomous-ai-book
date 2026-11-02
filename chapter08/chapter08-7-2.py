import socket


RASPBERRY_PI_IP = "192.168.128.152"
PORT = 5000


state = "no_person"


sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.connect(
    (RASPBERRY_PI_IP, PORT)
)

sock.sendall(
    state.encode("utf-8")
)

sock.close()

print(f"送信: {state}")
