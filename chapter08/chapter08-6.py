import socket

from gpiozero import LED


HOST = "0.0.0.0"
PORT = 5000


led = LED(17)


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))

server.listen(1)

print("サーバーを起動しました")
print(f"Port: {PORT}")


try:

    while True:

        conn, addr = server.accept()

        print(f"接続: {addr}")

        data = conn.recv(1024)

        if data:

            state = data.decode("utf-8")

            print(f"受信: {state}")


            if state == "person_detected":

                led.on()

                print("LED ON")


            elif state == "no_person":

                led.off()

                print("LED OFF")


        conn.close()


finally:

    led.off()

    server.close()
