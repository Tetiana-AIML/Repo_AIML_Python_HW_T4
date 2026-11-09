import sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def print_tree(directory, indent=""):
    try:
        folders = []
        files = []

        for item in directory.iterdir():
            if item.is_dir():
                folders.append(item)
            else:
                files.append(item)
    except PermissionError:
        print(indent + Fore.RED + "[немає доступу]")
        return

    items = folders + files

    for index, item in enumerate(items):
        is_last = index == len(items) - 1
        branch = "┗ " if is_last else "┣ "

        if item.is_dir():
            print(indent + branch + Style.BRIGHT + Fore.BLUE + f"📂{item.name}")
            
            new_indent = indent + ("  " if is_last else "┃ ")
            print_tree(item, new_indent)
        else:
            print(indent + branch + Fore.GREEN + f"📜{item.name}")

def main():
    if len(sys.argv) < 2:
        print(Fore.RED + "Вкажіть шлях до директорії.")
        return

    path = Path(sys.argv[1])

    if not path.exists():
        print(Fore.RED + f"Шлях '{path}' не існує.")
        return

    if not path.is_dir():
        print(Fore.RED + f"Шлях '{path}' не є директорією.")
        return

    print(Style.BRIGHT + Fore.BLUE + f"📦{path.name}")
    print_tree(path)


if __name__ == "__main__":
    main()