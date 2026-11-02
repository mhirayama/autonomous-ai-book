import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

ret, frame = cap.read()

if ret:
    print("フレームを取得しました")
    print("画像サイズ:", frame.shape)
else:
    print("フレームを取得できませんでした")

cap.release()
