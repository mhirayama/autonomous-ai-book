import cv2
import pymysql
from datetime import datetime
from ultralytics import YOLO


# -----------------------------
# YOLOモデル
# -----------------------------

model = YOLO("yolo11n.pt")


# -----------------------------
# MariaDB接続
# -----------------------------

connection = pymysql.connect(
    host="localhost",
    user="ai_user",
    password="ai_password",
    database="autonomous_ai",
    charset="utf8mb4"
)


# -----------------------------
# カメラ
# -----------------------------

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


if not cap.isOpened():
    print("カメラを開けませんでした")
    connection.close()
    exit()


print("自律型AIシステムを開始します")
print("qキーで終了します")


# -----------------------------
# メインループ
# -----------------------------

while True:

    # フレーム取得
    ret, frame = cap.read()

    if not ret:
        print("フレームを取得できませんでした")
        break


    # -------------------------
    # YOLO推論
    # -------------------------

    results = model(frame)
    result = results[0]


    # -------------------------
    # 人物情報
    # -------------------------

    people = []


    for box in result.boxes:

        class_id = int(box.cls[0])

        # 人物以外は無視
        if class_id != 0:
            continue


        # バウンディングボックス
        x1, y1, x2, y2 = box.xyxy[0].tolist()


        # 中心点
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)


        people.append({
            "x": center_x,
            "y": center_y
        })


    # -------------------------
    # 状態データ
    # -------------------------

    recorded_at = datetime.now()
    person_count = len(people)


    # -------------------------
    # MariaDBへ保存
    # -------------------------

    with connection.cursor() as cursor:

        sql = """
            INSERT INTO person_states
            (recorded_at, person_id, x, y, person_count)
            VALUES (%s, %s, %s, %s, %s)
        """


        for person_id, person in enumerate(people, start=1):

            cursor.execute(
                sql,
                (
                    recorded_at,
                    person_id,
                    person["x"],
                    person["y"],
                    person_count
                )
            )


    connection.commit()


    # -------------------------
    # 映像表示
    # -------------------------

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


    cv2.imshow(
        "Autonomous AI System",
        annotated_frame
    )


    # qキーで終了
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# 終了処理
# -----------------------------

cap.release()

cv2.destroyAllWindows()

connection.close()

print("自律型AIシステムを終了しました")
