from flask import Flask, request

from gpiozero import LED


app = Flask(__name__)


# ========================================
# GPIO設定
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

    # いったんLEDを停止
    led.off()


    if state == "empty":

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

        current_state = "empty"


    return current_state


# ========================================
# Raspberry Piの状態
# ========================================

@app.route(
    "/status",
    methods=["GET"]
)
def status():

    return {
        "status": "online",
        "state": current_state
    }


# ========================================
# 制御命令
# ========================================

@app.route(
    "/control",
    methods=["POST"]
)
def control():

    global current_state


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


    current_state = control_led(
        state
    )


    return {
        "status": "ok",
        "state": current_state
    }


# ========================================
# メイン
# ========================================

if __name__ == "__main__":

    try:

        app.run(
            host="0.0.0.0",
            port=5000
        )

    finally:

        led.off()
