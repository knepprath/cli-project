import subprocess
import shutil
import os
import urllib.request
from klickbrick import config


def execute(args):
    print(f"DEBUG : executing command {args}")
    if config.DRY_RUN:
        print(" ".join(args))
        return 0, "dry run"
    else:
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
    if config.DRY_RUN:
        print(f"cp {source} {destination}")
        return 0
    else:
        shutil.copyfile(
            f"{os.path.dirname(os.path.abspath(__file__))}/resources/{source}",
            destination,
        )


def install_from_url(executor, url):
    if config.DRY_RUN:
        print(f'/bin/{executor} -c "$(curl -fsSL {url})"')
        return 0
    else:
        print(f"DEBUG : Downloading installer from {url}")
        filename, headers = urllib.request.urlretrieve(url)
        print(f"DEBUG : Downloaded {filename} with headers {headers}")
        return_code, output = execute([executor, filename])
