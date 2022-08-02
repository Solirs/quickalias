#!/usr/bin/env python3
"""
This simple python script creates permenant aliases so you don't have to open your shell config file
"""
import os
import sys
import subprocess
import argparse

class QuickAlias:
    def __init__(self):
        pass

    def detect_shell(self) -> str:
        """ Detects the process calling the script """
        return os.environ.get("SHELL") or os.readlink(f'/proc/{os.getppid()}/exe')

def main() -> int:
    """
    the main method
    """

    # Creating an instance of the class `QuickAlias`
    quickalias = QuickAlias()

    # Creating a description for the script and then creating a parser for the arguments.
    module_description: str = "This script creates pemenant aliases so you don't have to."
    parser = argparse.ArgumentParser(description=module_description)
    parser.add_argument(
        "-a", "--alias", help="the alias for the command", required=False)
    parser.add_argument('alias', nargs='?',default=argparse.SUPPRESS)
    parser.add_argument("-c", "--command",
                        help="the command to be aliased", required=False)
    parser.add_argument('command', nargs='?',default=argparse.SUPPRESS)
    args = parser.parse_args()


    if args.alias and args.command:
        alias: str = args.alias
        command: str = args.command
    else:
        # Asking the user to input the alias and the command.
        alias: str = input('Enter alias for command: ')
        command: str = input('Enter the command: ')

    # Getting the home directory of the user.
    user_directory: str = os.path.expanduser('~')

    # Getting the process id of the parent process from proc.
    process_id: str = quickalias.detect_shell()

    if "bash" in process_id:
        shell: str = "bash"
        # Getting the path of the bashrc.
        shell_config_path: str = os.path.join(user_directory, '.bashrc')

    elif "zsh" in process_id:
        shell = "zsh"

        # Getting the path of the .zshrc file.
        shell_config_path: str = os.path.join(
            os.environ.get('ZDOTDIR') or user_directory, '.zshrc')
    elif "fish" in process_id:

        shell = "fish"
        # Getting the path of the config.fish file.
        shell_config_path: str = os.path.join(
            os.environ.get('XDG_CONFIG_HOME') or os.path.join(
                user_directory, '.config'), 'fish/config.fish')
    elif "ksh" in process_id:
        shell = "ksh"
        # Getting the path of the .kshrc file.
        shell_config_path: str = os.environ.get('ENV') or os.path.join(user_directory, '.kshrc')
    else:
        # If the shell is not detected, it will default to fish.
        shell: str = "bash"
        print("shell not detected. Defaulting to bash.")
        shell_config_path: str = None

    if shell_config_path is not None:
        config_location: str = shell_config_path
    else:
        config_location: str = f"{user_directory}/.bashrc"

    if shell in "bash" or shell in "zsh":
        alias_string: str = f"alias {alias}=\"{command}\""

        # This is checking if the alias already exists in the config file.
        # if it does, it will not add it again.
        with open(config_location, encoding="utf-8") as file:
            if alias_string in file.read():
                print(f"\n{alias} already exists in {config_location}")
                sys.exit(0)

        # Opening the config file in append mode and writing the alias to the file.
        with open(config_location, 'a', encoding="utf-8") as file:
            file.write(f"{alias_string}\n")
    elif shell in "ksh":
        alias_string: str = f"alias {alias}=\"{command}\""

        # This is checking if the alias already exists in the config file.
        # if it does, it will not add it again.
        with open(config_location, encoding="utf-8") as file:
            if alias_string in file.read():
                print(f"\n{alias} already exists in {config_location}")
                sys.exit(0)

        # Opening the config file in append mode and writing the alias to the file.
        with open(config_location, 'a', encoding="utf-8") as file:
            file.write(f"{alias_string}\n")

    else:
        # Running the fish shell with the `-c` flag, which allows you to run a command in the shell.
        subprocess.run(
            ["fish", "-c", f"alias --save {alias} \"{command}\""], check=True,
            stdout=subprocess.DEVNULL)

    print(f"\nAdded \"{alias_string}\" to shell config")

    source_command: str = f"source {config_location}"
    print(f"You can source the new changes with:\n\t{source_command}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
