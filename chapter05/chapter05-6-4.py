import cv2
from datetime import datetime
from ultralytics import YOLO


def judge_person_count(person_count):

    if person_count == 0:
        return "empty"

    elif person_count == 1:
        return "single"

    else:
        return "multiple"


def judge_position(x, y):

    if 0 <= x <= 300 and 0 <= y <= 300:
        return "inside"

    return "outside"


# YOLOモデル
model = YOLO("yolo11n.pt")


# カメラ
cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break


    # YOLO推論
    results = model(frame)
    result = results[0]


    people = []


    # 人物検出
    for box in result.boxes:

        class_id = int(box.cls[0])

        if class_id != 0:
            continue


        x1, y1, x2, y2 = box.xyxy[0].tolist()


        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)


        position_state = judge_position(
            center_x,
            center_y
        )


        people.append({
            "x": center_x,
            "y": center_y,
            "position_state": position_state
        })


    # 人数
    person_count = len(people)


    # 状態判断
    state = judge_person_count(person_count)


    # 状態データ
    state_data = {
        "recorded_at": datetime.now(),
        "person_count": person_count,
        "state": state,
        "people": people
    }


    print(state_data)


    # 映像表示
    annotated_frame = result.plot()


    cv2.putText(
        annotated_frame,
        f"People: {person_count}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    cv2.putText(
        annotated_frame,
        f"State: {state}",
        (10, 70),
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
