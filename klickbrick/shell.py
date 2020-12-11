import subprocess
import shutil
import os
import urllib.request


def execute(args):
    print(f"DEBUG : executing command {args}")
    try:
        output = subprocess.run(args, capture_output=True)
    except FileNotFoundError as exception:
        print(f"DEBUG : Failed to execute {args}")
        return exception.errno, exception.strerror
    print(f"DEBUG : stdout: {output.stdout}")
    if output.returncode != 0:
        print(f"DEBUG : stderr: {output.stderr}")
    return output.returncode, output.stdout.decode("utf-8")


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
