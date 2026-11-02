import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラを開けませんでした")
    exit()

print("カメラを開きました")

cap.release()
