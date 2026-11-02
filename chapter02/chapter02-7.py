import cv2
import time

# カメラを開く
cap = cv2.VideoCapture(0)

# 解像度を設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

print("カメラを開始しました")
print("qキーで終了します")

# FPS計測用
prev_time = time.time()

while True:
    # フレームを取得
    ret, frame = cap.read()

    if not ret:
        print("フレームを取得できませんでした")
        break

    # 現在時刻を取得
    current_time = time.time()

    # 経過時間を計算
    elapsed_time = current_time - prev_time

    # FPSを計算
    if elapsed_time > 0:
        fps = 1.0 / elapsed_time
    else:
        fps = 0

    prev_time = current_time

    # FPSを画面に表示
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # フレームを表示
    cv2.imshow("Camera", frame)

    # qキーで終了
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# カメラを解放
cap.release()

# ウィンドウを閉じる
cv2.destroyAllWindows()

print("カメラを終了しました")
