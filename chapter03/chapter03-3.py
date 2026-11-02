import cv2
from ultralytics import YOLO

# YOLOモデルを読み込む
model = YOLO("yolo11n.pt")

# カメラを開く
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

while True:
    # フレームを取得
    ret, frame = cap.read()

    if not ret:
        break

    # YOLOで推論
    results = model(frame)

    # 検出結果を描画
    annotated_frame = results[0].plot()

    # 映像を表示
    cv2.imshow("YOLO Camera", annotated_frame)

    # qキーで終了
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
