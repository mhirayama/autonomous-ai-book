from gpiozero import LED
from time import sleep

led = LED(17)

print("LEDを点灯します")

led.on()

sleep(3)

print("LEDを消灯します")

led.off()
