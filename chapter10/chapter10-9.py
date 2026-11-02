import cv2
import pymysql
import requests

from flask import (
    Flask,
    Response,
    render_template
)


# ========================================
# Flask
# ========================================

app = Flask(__name__)


# ========================================
# カメラ
# ========================================

camera = cv2.VideoCapture(0)


# ========================================
# Raspberry Pi
# ========================================

RASPBERRY_PI_IP = (
    "192.168.128.152"
)

RASPBERRY_PI_URL = (
    f"http://{RASPBERRY_PI_IP}:5000"
)


# ========================================
# MariaDB
# ========================================

DB_CONFIG = {
    "host": "localhost",
    "user": "ai_user",
    "password": "ai_password",
    "database": "autonomous_ai",
    "charset": "utf8mb4"
}


# ========================================
# Raspberry Pi状態
# ========================================

def get_raspberry_pi_status():

    try:

        response = requests.get(
            f"{RASPBERRY_PI_URL}/status",
            timeout=1
        )


        if response.status_code == 200:

            return response.json()


    except requests.RequestException:

        pass


    return {
        "status": "offline",
        "state": "unknown"
    }


# ========================================
# 現在のAI状態
# ========================================

def get_current_status():

    conn = pymysql.connect(
        **DB_CONFIG
    )


    try:

        with conn.cursor(
            pymysql.cursors.DictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    person_count,
                    state,
                    recorded_at
                FROM people_detection
                ORDER BY id DESC
                LIMIT 1
                """
            )


            row = cursor.fetchone()


            if row is not None:

                return row


    finally:

        conn.close()


    return {
        "person_count": 0,
        "state": "unknown",
        "recorded_at": None
    }


# ========================================
# AI判断メッセージ
# ========================================

def get_ai_message(state):

    if state == "empty":

        return "人物は検出されていません"


    elif state == "single":

        return "1人の人物を検出しています"


    elif state == "multiple":

        return "複数の人物を検出しています"


    else:

        return "状態を取得できません"


# ========================================
# LED状態
# ========================================

def get_led_status(state):

    if state == "empty":

        return "OFF"


    elif state == "single":

        return "ON"


    elif state == "multiple":

        return "BLINK"


    else:

        return "UNKNOWN"


# ========================================
# カメラ映像
# ========================================

def generate_frames():

    while True:

        success, frame = (
            camera.read()
        )


        if not success:

            break


        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )


        if not ret:

            continue


        frame_bytes = (
            buffer.tobytes()
        )


        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


# ========================================
# メイン画面
# ========================================

@app.route("/")
def index():

    status = get_current_status()

    raspberry_pi = (
        get_raspberry_pi_status()
    )


    ai_message = get_ai_message(
        status["state"]
    )


    led = get_led_status(
        raspberry_pi["state"]
    )


    return render_template(
        "index.html",
        person_count=status[
            "person_count"
        ],
        state=status[
            "state"
        ],
        ai_message=ai_message,
        raspberry_pi=raspberry_pi,
        led=led
    )


# ========================================
# カメラ映像
# ========================================

@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype=(
            "multipart/x-mixed-replace;"
            " boundary=frame"
        )
    )


# ========================================
# 起動
# ========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
