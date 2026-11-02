import time
import logging
import threading

import cv2
import pymysql
import psutil
import requests

from flask import Flask, render_template

from ultralytics import YOLO


# ==================================================
# Flask
# ==================================================

app = Flask(__name__)


# ==================================================
# 設定
# ==================================================

CAMERA_ID = 0

MODEL_PATH = "yolo11n.pt"

RASPBERRY_PI_IP = "192.168.128.152"

RASPBERRY_PI_URL = (
    f"http://{RASPBERRY_PI_IP}:5000"
)

TARGET_FPS = 5

RASPBERRY_PI_CHECK_INTERVAL = 2.0


# ==================================================
# MariaDB
# ==================================================

DB_HOST = "localhost"
DB_USER = "ai_user"
DB_PASSWORD = "ai_password"
DB_NAME = "autonomous_ai"


# ==================================================
# システム状態
# ==================================================

system_status = {

    "person_count": 0,
    "x": 0,
    "y": 0,
    "confidence": 0,
    "state": "empty",
    "led_state": "OFF",
    "processing_time": 0,
    "fps": 0,
    "cpu_usage": 0,
    "memory_usage": 0,
    "raspberry_pi_status": "OFFLINE"
}


status_lock = threading.Lock()


# ==================================================
# ログ
# ==================================================

logging.basicConfig(

    filename="system.log",

    level=logging.INFO,

    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(message)s"
    )
)


# ==================================================
# Flask
# ==================================================

@app.route("/")
def index():

    with status_lock:

        data = system_status.copy()

    return render_template(
        "index.html",
        **data
    )


# ==================================================
# 状態判断
# ==================================================

def judge_state(person_count):

    if person_count == 0:

        return "empty"

    elif person_count == 1:

        return "single"

    else:

        return "multiple"


# ==================================================
# LED状態
# ==================================================

def judge_led_state(state):

    if state == "empty":

        return "OFF"

    elif state == "single":

        return "ON"

    else:

        return "BLINK"


# ==================================================
# Raspberry Piへ状態送信
# ==================================================

def send_state(state):

    try:

        response = requests.post(

            f"{RASPBERRY_PI_URL}/control",

            json={
                "state": state
            },

            timeout=2
        )

        if response.ok:

            logging.info(
                f"Raspberry Pi: "
                f"state={state}"
            )

            return True

        logging.error(
            "Raspberry Pi returned error"
        )

        return False

    except requests.RequestException as e:

        logging.error(
            f"Raspberry Pi "
            f"connection error: {e}"
        )

        return False


# ==================================================
# Raspberry Pi状態確認
# ==================================================

def check_raspberry_pi():

    try:

        response = requests.get(

            f"{RASPBERRY_PI_URL}/status",

            timeout=2
        )

        return response.ok

    except requests.RequestException:

        return False


# ==================================================
# MariaDB接続
# ==================================================

def connect_database():

    return pymysql.connect(

        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4"
    )


# ==================================================
# データ保存
# ==================================================

def save_person_data(

    conn,
    person_count,
    x,
    y,
    confidence,
    state,
    led_state,
    processing_time

):

    try:

        with conn.cursor() as cursor:

            sql = """
            INSERT INTO system_events
            (
                recorded_at,
                person_count,
                x,
                y,
                confidence,
                state,
                led_state,
                processing_time
            )
            VALUES
            (
                NOW(),
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """

            cursor.execute(
                sql,
                (
                    person_count,
                    x,
                    y,
                    confidence,
                    state,
                    led_state,
                    processing_time
                )
            )

        conn.commit()

    except pymysql.MySQLError as e:

        logging.error(
            f"Database error: {e}"
        )

        try:

            conn.rollback()

        except pymysql.MySQLError:

            pass


# ==================================================
# AI処理
# ==================================================

def ai_loop():

    logging.info(
        "AI system started"
    )

    model = YOLO(
        MODEL_PATH
    )

    camera = cv2.VideoCapture(
        CAMERA_ID
    )

    if not camera.isOpened():

        logging.error(
            "Camera open failed"
        )

        return

    try:

        conn = connect_database()

        logging.info(
            "Database connected"
        )

    except pymysql.MySQLError as e:

        logging.error(
            f"Database connection failed: {e}"
        )

        camera.release()

        return

    previous_state = None

    frame_interval = (
        1 / TARGET_FPS
    )

    last_pi_check = 0

    raspberry_pi_status = "OFFLINE"

    try:

        while True:

            start_time = time.time()

            # ----------------------------------
            # カメラ入力
            # ----------------------------------

            success, frame = (
                camera.read()
            )

            if not success:

                logging.error(
                    "Camera read failed"
                )

                time.sleep(1)

                continue

            # ----------------------------------
            # YOLO推論
            # ----------------------------------

            results = model(
                frame,
                verbose=False
            )

            result = results[0]

            # ----------------------------------
            # 人物情報
            # ----------------------------------

            person_count = 0

            x = None
            y = None
            confidence = None

            if result.boxes is not None:

                for box in result.boxes:

                    class_id = int(
                        box.cls[0]
                    )

                    if class_id == 0:

                        person_count += 1

                        confidence = float(
                            box.conf[0]
                        )

                        x1, y1, x2, y2 = (
                            box.xyxy[0].tolist()
                        )

                        x = (
                            x1 + x2
                        ) / 2

                        y = (
                            y1 + y2
                        ) / 2

                        break

            # ----------------------------------
            # 状態判断
            # ----------------------------------

            state = judge_state(
                person_count
            )

            led_state = judge_led_state(
                state
            )

            # ----------------------------------
            # Raspberry Pi制御
            # ----------------------------------

            if state != previous_state:

                logging.info(

                    f"State changed: "
                    f"{previous_state} "
                    f"-> {state}"
                )

                if send_state(state):

                    previous_state = state

            # ----------------------------------
            # CPU・メモリ
            # ----------------------------------

            cpu_usage = (
                psutil.cpu_percent(
                    interval=None
                )
            )

            memory_usage = (
                psutil.virtual_memory()
                .percent
            )

            # ----------------------------------
            # Raspberry Pi状態確認
            # ----------------------------------

            current_time = time.time()

            if (
                current_time
                - last_pi_check
                >= RASPBERRY_PI_CHECK_INTERVAL
            ):

                raspberry_pi_online = (
                    check_raspberry_pi()
                )

                raspberry_pi_status = (

                    "ONLINE"
                    if raspberry_pi_online
                    else "OFFLINE"
                )

                last_pi_check = (
                    current_time
                )

            # ----------------------------------
            # 処理時間
            # ----------------------------------

            processing_time = (
                time.time()
                - start_time
            )

            fps = (

                1 / processing_time
                if processing_time > 0
                else 0
            )

            # ----------------------------------
            # MariaDB保存
            # ----------------------------------

            save_person_data(

                conn,

                person_count,

                x,

                y,

                confidence,

                state,

                led_state,

                processing_time
            )

            # ----------------------------------
            # Web画面用状態更新
            # ----------------------------------

            with status_lock:

                system_status[
                    "person_count"
                ] = person_count

                system_status[
                    "x"
                ] = x

                system_status[
                    "y"
                ] = y

                system_status[
                    "confidence"
                ] = confidence

                system_status[
                    "state"
                ] = state

                system_status[
                    "led_state"
                ] = led_state

                system_status[
                    "processing_time"
                ] = processing_time

                system_status[
                    "fps"
                ] = fps

                system_status[
                    "cpu_usage"
                ] = cpu_usage

                system_status[
                    "memory_usage"
                ] = memory_usage

                system_status[
                    "raspberry_pi_status"
                ] = raspberry_pi_status

            # ----------------------------------
            # 映像表示
            # ----------------------------------

            annotated_frame = (
                result.plot()
            )

            cv2.putText(
                annotated_frame,
                f"People: {person_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                annotated_frame,
                f"State: {state}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                annotated_frame,
                f"FPS: {fps:.1f}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "Autonomous AI System",
                annotated_frame
            )

            # ----------------------------------
            # FPS制御
            # ----------------------------------

            elapsed_time = (
                time.time()
                - start_time
            )

            sleep_time = (
                frame_interval
                - elapsed_time
            )

            if sleep_time > 0:

                time.sleep(
                    sleep_time
                )

            # ----------------------------------
            # 終了
            # ----------------------------------

            key = (
                cv2.waitKey(1)
                & 0xFF
            )

            if key == ord("q"):

                break

    except KeyboardInterrupt:

        logging.info(
            "System stopped by user"
        )

    except Exception as e:

        logging.exception(
            f"Unexpected error: {e}"
        )

    finally:

        logging.info(
            "System shutdown started"
        )

        camera.release()

        cv2.destroyAllWindows()

        conn.close()

        # 終了時にLEDを消灯

        send_state(
            "empty"
        )

        logging.info(
            "System shutdown complete"
        )


# ==================================================
# 実行
# ==================================================

if __name__ == "__main__":

    ai_thread = threading.Thread(
        target=ai_loop,
        daemon=True
    )

    ai_thread.start()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
