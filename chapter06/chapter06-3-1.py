import cv2


state = "occupied"


cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break


    if state == "empty":
        message = "EMPTY"

    elif state == "single":
        message = "SINGLE"

    else:
        message = "MULTIPLE"


    cv2.putText(
        frame,
        f"State: {message}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    cv2.imshow(
        "Autonomous AI System",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
