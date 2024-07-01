from colorama import Fore, Back, Style


def Warning(text: str):
    print(Fore.YELLOW + '[Waring]:' + text + Fore.RESET)


def Error(text: str):
    print(Fore.RED + '[Error]:' + text + Fore.RESET)


def Info(text: str):
    print(Fore.WHITE + '[Info]:' + text + Fore.RESET)

def Data(text: str):
    print(Fore.LIGHTWHITE_EX + '[Data]:' + text + Fore.RESET)

def Content(text: str):
    print(Fore.WHITE + text + Fore.RESET)

def Config(text: str):
    print(Fore.WHITE + '[Config]:' + text + Fore.RESET)

def Notice(text: str):
    print(Fore.YELLOW + '[Notice]:' + text + Fore.RESET)

def Status(text: str):
    print(Fore.GREEN + text + Fore.RESET)

def Processing(text: str):
    print(Fore.GREEN + text + Fore.RESET)


def Successfully(text: str):
    print(Fore.LIGHTYELLOW_EX + text + Fore.RESET)
