person_count = 2

if person_count == 0:
    state = "empty"

elif person_count == 1:
    state = "single"

else:
    state = "multiple"

print("人数:", person_count)
print("状態:", state)
