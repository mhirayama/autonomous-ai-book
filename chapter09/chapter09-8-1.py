import socket

from gpiozero import LED


HOST = "0.0.0.0"
PORT = 5000


led = LED(17)


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(
    (HOST, PORT)
)

server.listen(1)


print("Raspberry Pi server")
print(f"Port: {PORT}")


try:

    while True:

        conn, addr = server.accept()

        data = conn.recv(1024)

        if data:

            command = data.decode(
                "utf-8"
            )

            print(
                f"Received: {command}"
            )


            if command == "no_person":

                led.off()


            elif command == "person_detected":

                led.on()


            elif command == "multiple_people":

                led.blink(
                    on_time=0.5,
                    off_time=0.5
                )


        conn.close()


finally:

    led.off()

    server.close()
