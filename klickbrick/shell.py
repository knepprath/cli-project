import subprocess


def execute(args):
    print(f"DEBUG: executing command {args}")
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    print(f"DEBUG : stdout: {stdout}")
    if process.returncode != 0:
        print(f"DEBUG : stderr: {stderr}")
    return process.returncode, stdout.decode("utf-8")
