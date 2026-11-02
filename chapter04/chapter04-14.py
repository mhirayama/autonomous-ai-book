import pymysql


connection = pymysql.connect(
    host="localhost",
    user="ai_user",
    password="ai_password",
    database="autonomous_ai",
    charset="utf8mb4"
)

print("MariaDBへの接続に成功しました")

connection.close()
