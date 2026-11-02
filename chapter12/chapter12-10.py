from flask import Flask, request
from gpiozero import LED


app = Flask(__name__)

led = LED(17)

current_state = "empty"


@app.route("/status", methods=["GET"])
def status():

    return {
        "status": "online",
        "state": current_state
    }


@app.route("/control", methods=["POST"])
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

    if state == "empty":

        led.off()

    elif state == "single":

        led.on()

    elif state == "multiple":

        led.blink(
            on_time=0.5,
            off_time=0.5
        )

    else:

        led.off()

        state = "empty"

    current_state = state

    return {
        "status": "ok",
        "state": current_state
    }


if __name__ == "__main__":

    try:

        app.run(
            host="0.0.0.0",
            port=5000
        )

    finally:

        led.off()
