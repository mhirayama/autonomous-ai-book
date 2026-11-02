def judge_person_count(person_count):

    if person_count == 0:
        return "empty"

    elif person_count == 1:
        return "single"

    else:
        return "multiple"
        
def judge_position(x, y):

    if 0 <= x <= 300 and 0 <= y <= 300:
        return "inside"

    return "outside"
    
from datetime import datetime


people = [
    {"x": 210, "y": 250},
    {"x": 470, "y": 230}
]


# 人数
person_count = len(people)


# 人数による状態判断
person_state = judge_person_count(person_count)


# 位置による判断
for person in people:

    person["position_state"] = judge_position(
        person["x"],
        person["y"]
    )


# 状態データ
state_data = {
    "recorded_at": datetime.now(),
    "person_count": person_count,
    "state": person_state,
    "people": people
}


print(state_data)
