import os
import subprocess

audio_path = os.path.join(os.path.dirname(__file__), "up", "Allure.mp3")
subprocess.run(["mpg123", audio_path])
