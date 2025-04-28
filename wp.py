import base64
import os
import sys


def create_wrapper(file_path):
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # 압축하여 base64 인코딩
    compressed_data = base64.b64encode(file_data).decode("utf-8")

    execute_command = f"""
import base64
import io
import subprocess
import sys
import os

FILE_DATA = "{compressed_data}"
DATA = base64.b64decode(FILE_DATA)

try:
    # 메모리에서 파일 실행 (파이썬 코드로 간주)
    CODE = DATA.decode("utf-8")
    exec(CODE)

except Exception as e:
    print(f"Error executing: {{e}}")
    sys.exit(1)
"""

    wrapper_script = f"""
import base64
import os
import subprocess
import sys
import platform
import stat
import shutil

{execute_command}
"""

    return wrapper_script

while True:
    FILE_PATH = input("type file path:").strip().strip('"')
    if os.path.exists(FILE_PATH):
        break
    else:
        print("wrong command")

while True:
    NAME = input("type py file name: ")
    if NAME:
        break
    else:
        print("file name is needed")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, f"{NAME}.py")

if os.path.exists(file_path):
    print(f"{NAME}.py already exists on the desktop. Please delete it first.")
    sys.exit(1)

wrapper_script = create_wrapper(FILE_PATH)
with open(file_path, "w") as f:
    f.write(wrapper_script)

print("!done! File created on desktop.")
