def judge_person_state(person_count):

    if person_count == 0:
        return "empty"

    elif person_count == 1:
        return "single"

    else:
        return "multiple"


person_count = 2

state = judge_person_state(person_count)

print(state)
