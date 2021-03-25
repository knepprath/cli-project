import subprocess
import os
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
    command = f"cp {source} {destination}"
    logging.debug(f"copying {source} to {destination}")
    if config.DRY_RUN:
        print(command)
        return True
    else:
        return_code, output = execute(command)
        if return_code == 0:
            return True
        else:
            return False


def install_from_url(executor, url, args=""):
    command = f'{executor} -c "$(curl -fsSL {url})" {args}'
    logging.debug(f"downloading from {url} and executing with {executor}")
    if config.DRY_RUN:
        print(command)
        return 0
    else:
        execute(command)


def create_directory(path):
    command = f"mkdir -p {path}"
    logging.debug(f"creating the directory {path}")

    if os.path.isdir(path):
        logging.error(f"The directory already exists: {path}")
        return False
    else:
        if config.DRY_RUN:
            print(command)
        else:
            execute(command)
        return True


def append_to_file(path, content):
    command = f"echo '\n{content}\n' >> {path}"
    logging.debug(f"append to {path} the following content: {content}")
    if config.DRY_RUN:
        print(command)
        return 0
    else:
        execute(command)
