import cv2
from ultralytics import YOLO


def judge_person_count(person_count):

    if person_count == 0:
        return "empty"

    elif person_count == 1:
        return "single"

    else:
        return "multiple"


model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break


    results = model(frame)

    result = results[0]


    people = []


    for box in result.boxes:

        class_id = int(box.cls[0])

        if class_id != 0:
            continue


        people.append(box)


    person_count = len(people)

    state = judge_person_count(person_count)


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


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
