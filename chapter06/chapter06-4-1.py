import time


state = "empty"


if state == "empty":
    interval = 2.0

else:
    interval = 0.5


print(f"処理間隔: {interval}秒")

time.sleep(interval)
