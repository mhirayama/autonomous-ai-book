import time
import socket
from datetime import datetime
import cv2
import pymysql

from ultralytics import YOLO


# ========================================
# 設定
# ========================================

CAMERA_ID = 0

MODEL_PATH = "yolo11n.pt"

RASPBERRY_PI_IP = "192.168.128.152"
RASPBERRY_PI_PORT = 5000


DB_HOST = "localhost"
DB_USER = "ai_user"
DB_PASSWORD = "ai_password"
DB_NAME = "autonomous_ai"


# ========================================
# YOLO
# ========================================

model = YOLO(MODEL_PATH)


# ========================================
# MariaDB
# ========================================

conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset="utf8mb4"
)

cursor = conn.cursor()


# ========================================
# カメラ
# ========================================

cap = cv2.VideoCapture(
    CAMERA_ID
)


# ========================================
# 状態判断
# ========================================

def judge_state(person_count):

    if person_count == 0:

        return "empty"


    elif person_count == 1:

        return "single"


    else:

        return "multiple"


# ========================================
# Raspberry Piへ命令を送信
# ========================================

def send_command(command):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.connect(
        (
            RASPBERRY_PI_IP,
            RASPBERRY_PI_PORT
        )
    )

    sock.sendall(
        command.encode("utf-8")
    )

    sock.close()


# ========================================
# メイン処理
# ========================================

previous_state = None


try:

    while True:

        # --------------------------------
        # カメラ入力
        # --------------------------------

        ret, frame = cap.read()

        if not ret:

            break


        # --------------------------------
        # YOLO推論
        # --------------------------------

        results = model(frame)

        result = results[0]


        # --------------------------------
        # 人物情報
        # --------------------------------

        person_count = 0

        person_positions = []


        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )


            if class_id == 0:

                person_count += 1


                x1, y1, x2, y2 = (
                    box.xyxy[0]
                )


                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)


                center_x = (
                    x1 + x2
                ) // 2


                center_y = (
                    y1 + y2
                ) // 2


                person_positions.append(
                    (
                        center_x,
                        center_y
                    )
                )


        # --------------------------------
        # 状態判断
        # --------------------------------

        state = judge_state(
            person_count
        )


        print(
            f"People: {person_count}, "
            f"State: {state}"
        )


        # --------------------------------
        # データベース保存
        # --------------------------------
        
        recorded_at = datetime.now()
        
        if person_positions:

            for center_x, center_y in person_positions:

                sql = """
                INSERT INTO people_detection
                (
                    recorded_at,
                    person_count,
                    center_x,
                    center_y,
                    state
                )
                VALUES
                (
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
                        recorded_at,
                        person_count,
                        center_x,
                        center_y,
                        state
                    )
                )

        else:

            sql = """
            INSERT INTO people_detection
            (
                recorded_at,
                person_count,
                center_x,
                center_y,
                state
            )
            VALUES
            (
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
                    recorded_at,
                    person_count,
                    None,
                    None,
                    state
                )
            )

        conn.commit()

        # --------------------------------
        # 状態変化時のみRaspberry Piを制御
        # --------------------------------

        if state != previous_state:

            if state == "empty":

                command = "no_person"


            elif state == "single":

                command = "person_detected"


            else:

                command = "multiple_people"


            try:

                send_command(
                    command
                )

                print(
                    f"Command: {command}"
                )


            except Exception as e:

                print(
                    f"Raspberry Pi error: {e}"
                )


            previous_state = state


        # --------------------------------
        # 映像表示
        # --------------------------------

        annotated_frame = result.plot()


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


        cv2.imshow(
            "Autonomous AI System",
            annotated_frame
        )


        # --------------------------------
        # 終了
        # --------------------------------

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


finally:

    cap.release()

    cv2.destroyAllWindows()

    cursor.close()

    conn.close()
