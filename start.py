import subprocess


def run_as_admin(command):
    try:
        subprocess.run(["cmd.exe", "/c", command], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

run_as_admin(f"log_service.exe start")
