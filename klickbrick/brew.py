from klickbrick import shell
import logging


def install(package_name):
    logging.info(f"Using brew to install {package_name}")
    return_code, output = shell.execute(["brew", "install", package_name])

    if return_code != 0:
        logging.error(f"The packages {package_name} was not installed")

    return_code, output = shell.execute([package_name, "--version"])
    logging.debug(f"Installed {package_name} version {output}")
