import subprocess
from pathlib import Path

import shutil
import os
import urllib.request
import logging
from klickbrick import config


def execute(args):
    logging.debug(f"executing command `{args}`")
    if config.DRY_RUN:
        print(args)
        return 0, "Invoked using dry run"
    else:
        try:
            output = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                executable="/bin/bash",
            )
        except FileNotFoundError as exception:
            logging.error(f"Failed to execute {args}")
            return exception.errno, exception.strerror
        logging.debug(f"stdout: {output.stdout}")
        if output.returncode != 0:
            logging.error(f"stderr: {output.stdout}")
        return output.returncode, output.stdout.decode("utf-8")


def copy_file(source, destination):
    logging.debug(f"copying {source} to {destination}")
    if config.DRY_RUN:
        print(f"cp {source} {destination}")
        return 0
    else:
        shutil.copyfile(
            f"{os.path.dirname(os.path.abspath(__file__))}/resources/{source}",
            destination,
        )


def install_from_url(executor, url, args=""):
    logging.debug(f"downloading from {url} and executing with {executor}")
    if config.DRY_RUN:
        print(f'{executor} -c "$(curl -fsSL {url})" {args}')
        return 0
    else:
        logging.debug(f"Downloading installer from {url}")
        filename, headers = urllib.request.urlretrieve(url)
        logging.debug(f"Downloaded {filename} with headers {headers}")
        execute(f"{executor} {filename} {args}")


def create_directory(path):
    logging.debug(f"creating the directory {path}")

    if os.path.isdir(path):
        logging.error(
            f"Cannot create project. The directory already exits: {path}"
        )
    else:
        if config.DRY_RUN:
            print(f"mkdir -p {path}")
            return 0
        else:
            Path(path).mkdir(parents=True)


def append_to_file(path, content):
    logging.debug(f"append to {path} the following content: {content}")
    if config.DRY_RUN:
        print(f"echo {content} >> {path}")
        return 0
    else:
        with open(path, "a") as file:
            file.write(content)
