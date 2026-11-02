import cv2
import requests

from ultralytics import YOLO


# ========================================
# 設定
# ========================================

MODEL_PATH = "yolo11n.pt"

CAMERA_ID = 0

RASPBERRY_PI_IP = "192.168.128.152"

RASPBERRY_PI_URL = (
    f"http://{RASPBERRY_PI_IP}:5000"
)


# ========================================
# YOLO
# ========================================

model = YOLO(
    MODEL_PATH
)


# ========================================
# カメラ
# ========================================

camera = cv2.VideoCapture(
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
# 観測
# ========================================

def observe():

    success, frame = camera.read()


    if not success:

        return None, None


    results = model(
        frame,
        verbose=False
    )


    result = results[0]


    person_count = 0


    if result.boxes is not None:

        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )


            # COCOのperson = 0

            if class_id == 0:

                person_count += 1


    return (
        person_count,
        result
    )


# ========================================
# Raspberry Piへの制御命令
# ========================================

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

            print(
                f"Raspberry Piへ送信: {state}"
            )

            return True


        print(
            "制御命令の送信に失敗しました"
        )

        return False


    except requests.RequestException as e:

        print(
            f"通信エラー: {e}"
        )

        return False


# ========================================
# フィードバックループ
# ========================================

previous_state = None


try:

    while True:

        # -------------------------------
        # 1. 観測
        # -------------------------------

        person_count, result = (
            observe()
        )


        if person_count is None:

            print(
                "カメラから映像を取得できません"
            )

            break


        # -------------------------------
        # 2. 判断
        # -------------------------------

        state = judge_state(
            person_count
        )


        # -------------------------------
        # 3. 状態変化を確認
        # -------------------------------

        if state != previous_state:

            print(
                "===================="
            )


            print(
                f"人物数: {person_count}"
            )


            print(
                f"状態: {state}"
            )


            # ---------------------------
            # 4. 制御
            # ---------------------------

            send_state(
                state
            )


            # ---------------------------
            # 5. 前回状態を更新
            # ---------------------------

            previous_state = state


        # -------------------------------
        # 6. 映像表示
        # -------------------------------

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


        cv2.imshow(
            "Feedback AI System",
            annotated_frame
        )


        # -------------------------------
        # 7. 終了
        # -------------------------------

        if (
            cv2.waitKey(1) & 0xFF
            == ord("q")
        ):

            break


finally:

    camera.release()

    cv2.destroyAllWindows()
