def judge_person_count(person_count):

    if person_count == 0:
        return "empty"

    elif person_count == 1:
        return "single"

    else:
        return "multiple"

person_count = 2

state = judge_person_count(person_count)

if state == "empty":
    print("待機します")

elif state == "single":
    print("通常処理を実行します")

elif state == "multiple":
    print("詳細処理を実行します")
