from datetime import datetime

people = [
    {"x": 210, "y": 250},
    {"x": 470, "y": 230}
]

state = {
    "recorded_at": datetime.now(),
    "person_count": len(people),
    "people": people
}

print(state)
