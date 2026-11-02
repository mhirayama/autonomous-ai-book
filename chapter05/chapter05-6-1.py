people = [
    {"x": 210, "y": 250},
    {"x": 470, "y": 230}
]

person_count = len(people)

if person_count == 0:
    state = "empty"

elif person_count == 1:
    state = "single"

else:
    state = "multiple"


from datetime import datetime


state_data = {
    "recorded_at": datetime.now(),
    "person_count": person_count,
    "state": state
}

print(state_data)
