import cv2
import time
from ultralytics import YOLO


def judge_person_count(person_count):

    if person_count == 0:
        return "empty"

    elif person_count == 1:
        return "single"

    else:
        return "multiple"


def get_interval(state):

    if state == "empty":
        return 2.0

    elif state == "single":
        return 0.5

    elif state == "multiple":
        return 0.2

    return 1.0


def get_message(state):

    if state == "empty":
        return "WAITING"

    elif state == "single":
        return "MONITORING"

    elif state == "multiple":
        return "ALERT"

    return "UNKNOWN"


model = YOLO("yolo11n.pt")


cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()


last_process_time = 0


while True:

    ret, frame = cap.read()

    if not ret:
        break


    current_time = time.time()


    # -----------------------------
    # 現在の状態
    # -----------------------------

    # 最初は現在のフレームを処理
    if current_time - last_process_time >= 0:

        results = model(frame)

        result = results[0]


        people = []


        for box in result.boxes:

            class_id = int(box.cls[0])

            if class_id != 0:
                continue

            people.append(box)


        person_count = len(people)


        # -------------------------
        # 状態判断
        # -------------------------

        state = judge_person_count(
            person_count
        )


        # -------------------------
        # 状態による制御
        # -------------------------

        interval = get_interval(state)

        message = get_message(state)


        last_process_time = current_time


    # -----------------------------
    # 映像表示
    # -----------------------------

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


    cv2.putText(
        annotated_frame,
        f"Mode: {message}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    cv2.putText(
        annotated_frame,
        f"Interval: {interval:.1f}s",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    cv2.imshow(
        "Autonomous AI System",
        annotated_frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()
