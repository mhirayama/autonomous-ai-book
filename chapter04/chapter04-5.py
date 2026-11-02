from datetime import datetime


def create_state(people):

    state = {
        "recorded_at": datetime.now(),
        "person_count": len(people),
        "people": people
    }

    return state

people = [
    {"x": 210, "y": 250},
    {"x": 470, "y": 230}
]

state = create_state(people)

print(state)
