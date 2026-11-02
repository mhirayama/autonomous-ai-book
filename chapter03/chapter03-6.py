import cv2
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

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

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        people.append({
            "x": center_x,
            "y": center_y
        })

    print("人数:", len(people))
    print("位置:", people)

    annotated_frame = result.plot()

    cv2.imshow("YOLO Camera", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
