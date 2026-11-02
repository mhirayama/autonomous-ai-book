import sys
import platform


print(
    "=== 自律型AIシステム "
    "開発環境チェック ==="
)

print()

print(
    f"Python : {sys.version}"
)

print(
    f"OS     : {platform.system()}"
)

print(
    f"Machine: {platform.machine()}"
)

print()

print(
    "Pythonの実行環境を確認しました。"
)
