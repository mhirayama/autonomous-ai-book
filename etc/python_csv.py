import pymysql
import csv

conn = pymysql.connect(
    host="localhost",
    user="ai_user",
    password="ai_password",
    database="autonomous_ai"
)

cursor = conn.cursor()

cursor.execute("""
    SELECT
 recorded_at,
                person_count,
                x,
                y,
                confidence,
                state,
                led_state,
                processing_time
    FROM system_events
    ORDER BY recorded_at
""")

rows = cursor.fetchall()

with open("people_detection.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
 "recorded_at",
                "person_count",
                "x",
                "y",
                "confidence",
                "state",
                "led_state",
                "processing_time"
    ])

    writer.writerows(rows)

cursor.close()
conn.close()

print("CSVを出力しました。")
