from gpiozero import LED
from time import sleep

led = LED(17)

previous_state = None

state = "single"

if state != previous_state:

    if state == "empty":
        led.off()

    elif state == "single":
        led.on()

    elif state == "multiple":
        led.blink(
            on_time=0.5,
            off_time=0.5
        )

    previous_state = state

sleep(10)

led.off()
