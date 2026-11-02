import pymysql
from datetime import datetime


connection = pymysql.connect(
    host="localhost",
    user="ai_user",
    password="ai_password",
    database="autonomous_ai",
    charset="utf8mb4"
)


people = [
    {"x": 210, "y": 250},
    {"x": 470, "y": 230}
]


recorded_at = datetime.now()
person_count = len(people)


with connection.cursor() as cursor:

    sql = """
        INSERT INTO person_states
        (recorded_at, person_id, x, y, person_count)
        VALUES (%s, %s, %s, %s, %s)
    """

    for person_id, person in enumerate(people, start=1):

        cursor.execute(
            sql,
            (
                recorded_at,
                person_id,
                person["x"],
                person["y"],
                person_count
            )
        )


connection.commit()
connection.close()

print("データを保存しました")
