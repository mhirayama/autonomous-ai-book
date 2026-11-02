from gpiozero import LED
from time import sleep

led = LED(17)

def control_led(state):

    if state == "empty":
        led.off()

    elif state == "single":
        led.on()

    elif state == "multiple":
        led.blink(
            on_time=0.5,
            off_time=0.5
        )

state = "single"

control_led(state)

sleep(10)

led.off()
