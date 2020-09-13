from klickbrick import shell


def install(package_name):
    return_code, output = shell.execute(["command", "-v", package_name])

    if return_code == 0:
        print(f"DEBUG : The package {package_name} is already installed")
    else:
        return_code, output = shell.execute(["brew", "install", package_name])

        if return_code != 0:
            print(f"ERROR : the packages {package_name} was not installed")

    return_code, output = shell.execute([package_name, "--version"])
    print(f"DEBUG : installed {package_name} version {output}")
