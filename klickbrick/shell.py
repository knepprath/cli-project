import subprocess

import shutil
import os
import urllib.request
import logging
from klickbrick import config


def execute(args):
    logging.debug(f"executing command {args}")
    if config.DRY_RUN:
        print(" ".join(args))
        return 0, "Invoked using dry run"
    else:
        try:
            output = subprocess.run(
                args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        except FileNotFoundError as exception:
            logging.error(f"Failed to execute {args}")
            return exception.errno, exception.strerror
        logging.debug(f"stdout: {output.stdout}")
        if output.returncode != 0:
            logging.error(f"stderr: {output.stdout}")
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
        logging.debug(f"Downloading installer from {url}")
        filename, headers = urllib.request.urlretrieve(url)
        logging.debug(f"Downloaded {filename} with headers {headers}")
        execute([executor, filename])
