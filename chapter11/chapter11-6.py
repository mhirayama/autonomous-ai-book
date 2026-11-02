from flask import Flask, request

from gpiozero import LED


# ========================================
# Flask
# ========================================

app = Flask(__name__)


# ========================================
# GPIO
# ========================================

led = LED(17)


# ========================================
# 現在の状態
# ========================================

current_state = "empty"


# ========================================
# LED制御
# ========================================

def control_led(state):

    global current_state


    # 現在の状態を停止

    led.off()


    if state == "empty":

        led.off()

        current_state = "empty"


    elif state == "single":

        led.on()

        current_state = "single"


    elif state == "multiple":

        led.blink(
            on_time=0.5,
            off_time=0.5
        )

        current_state = "multiple"


    else:

        led.off()

        current_state = "empty"


# ========================================
# 制御API
# ========================================

@app.route(
    "/control",
    methods=["POST"]
)
def control():

    data = request.get_json(
        silent=True
    )


    if data is None:

        return {
            "status": "error",
            "message": "Invalid JSON"
        }, 400


    state = data.get(
        "state",
        "empty"
    )


    control_led(
        state
    )


    return {
        "status": "ok",
        "state": current_state
    }


# ========================================
# 状態確認API
# ========================================

@app.route(
    "/status",
    methods=["GET"]
)
def status():

    if current_state == "empty":

        led_state = "OFF"


    elif current_state == "single":

        led_state = "ON"


    else:

        led_state = "BLINK"


    return {
        "status": "online",
        "state": current_state,
        "led": led_state
    }


# ========================================
# 起動
# ========================================

if __name__ == "__main__":

    try:

        app.run(
            host="0.0.0.0",
            port=5000
        )

    finally:

        led.off()
