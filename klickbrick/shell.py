import subprocess
import os

from klickbrick import config


def execute(args):
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
            return exception.errno, exception.strerror
        return output.returncode, output.stdout.decode("utf-8")


def copy_file(source, destination):
    command = f"cp {source} {destination}"
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
    if config.DRY_RUN:
        print(command)
        return 0
    else:
        execute(command)


def create_directory(path):
    command = f"mkdir -p {path}"

    if os.path.isdir(path):
        return False
    else:
        if config.DRY_RUN:
            print(command)
        else:
            execute(command)
        return True


def append_to_file(path, content):
    command = f"echo '\n{content}\n' >> {path}"
    if config.DRY_RUN:
        print(command)
        return 0
    else:
        execute(command)
