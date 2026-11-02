import cv2

from ultralytics import YOLO


# ========================================
# 設定
# ========================================

MODEL_PATH = "yolo11n.pt"

CAMERA_ID = 0


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
# 環境を観測
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
    
person_count, result = observe()

print(person_count)
