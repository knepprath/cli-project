import subprocess
import shutil
import os
import urllib.request


def execute(args):
    print(f"DEBUG : executing command {args}")
    try:
        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except FileNotFoundError as exception:
        print(f"DEBUG : Failed to execute {args}")
        return exception.errno, exception.strerror
    stdout, stderr = process.communicate()
    print(f"DEBUG : stdout: {stdout}")
    if process.returncode != 0:
        print(f"DEBUG : stderr: {stderr}")
    return process.returncode, stdout.decode("utf-8")


def copy_file(source, destination):
    shutil.copyfile(
        f"{os.path.dirname(os.path.abspath(__file__))}/resources/{source}",
        destination,
    )


def install_from_url(executor, url):
    print(f"DEBUG : Downloading installer from {url}")
    filename, headers = urllib.request.urlretrieve(url)
    print(f"DEBUG : Downloaded {filename} with headers {headers}")
    return_code, output = execute([executor, filename])
