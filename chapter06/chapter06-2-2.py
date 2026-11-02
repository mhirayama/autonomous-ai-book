def empty_mode():
    print("待機モード")


def single_mode():
    print("通常モード")


def multiple_mode():
    print("詳細モード")
    
state = "multiple"

if state == "empty":
    empty_mode()

elif state == "single":
    single_mode()

elif state == "multiple":
    multiple_mode()
