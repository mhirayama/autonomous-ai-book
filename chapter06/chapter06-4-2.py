import time


def get_interval(state):

    if state == "empty":
        return 2.0

    elif state == "single":
        return 0.5

    elif state == "multiple":
        return 0.2

    return 1.0
    
state = "multiple"

interval = get_interval(state)

print("処理間隔:", interval)

time.sleep(interval)
