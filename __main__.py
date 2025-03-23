#!/usr/bin/python3
"""
This program search and count files or file sizes in directories with filters
---------------------------------------------------------------------------------
Muuur - 2020
---------------------------------------------------------------------------------
"""

from sys import argv, stderr
from os import scandir
from re import sub
from pathlib import Path
from typing import NoReturn
from colorama import init, Fore
from enums import *
from mainclass import *

def die(msg: str, code: int=1) -> NoReturn:
    """
    Print an error message to stderr, help recommendation and exit
    
    Parameters
    ----------
    msg: str
        The message to display before exiting

    code: int = 1
        The status code for sys.exit(), default 1
    
    Returns
    -------
    NoReturn
    """
    print(sub(r'^ *', '', msg), file=stderr, end="\n\n")
    print(f"Please write `{Path(argv[0]).name} --help` to get help", file=stderr)
    exit(code)

def main(argv: list[str]=argv) -> int:
    """
    Main function, it performs all of the operations to count files or size
    
    Parameters
    ----------
    argv: list[str] = argv
        Console arguments, default sys.argv

    Returns
    -------
    main: int
        Status code, 0 if no error happened, 1 otherwise
    """
    init()
    aux, sumsize = 0, 0

    if len(argv) == 1:
        # ? Default (show all separated)
        dir, files, links = 0, 0, 0
        for i in scandir():
            if i.is_symlink():
                links += 1
            elif i.is_file():
                files += 1
            elif i.is_dir():
                dir += 1
        print(
            f"""There are {dir + files + links} elements in this directory
            \t{dir} {Fore.LIGHTBLUE_EX}folders{Fore.RESET}
            \t{files} {Fore.LIGHTGREEN_EX}files{Fore.RESET}
            \t{links} {Fore.LIGHTCYAN_EX}symbolic links{Fore.RESET}
        """.replace("  ", ''), end="")
        return 0

    # ? Argument parsing
    argvcont = ArgvContainer.parse_args(argv[1:])

    # ! Restrictions
    if argvcont.separate and argvcont.blank:
        die(f"many: You {Fore.RED}cannot{Fore.RESET} separate output and run it blank, -s is incompatible with -n")
    elif argvcont.separate and (not argvcont.recr and len(argvcont) == 1):
        die(f"many: You {Fore.RED}must specify{Fore.RED} -r or at least two {Fore.LIGHTGREEN_EX}filters{Fore.RESET} to use -s")
    elif argvcont.ftype & FileType.LINK and argvcont.follow:
        print(f"many: {Fore.LIGHTMAGENTA_EX}warning{Fore.RESET} you {Fore.RED}can't{Fore.RESET} count symbolic links while follow them, -l is {Fore.RED}incompatible{Fore.RESET} with -f", file=stderr)
        argvcont.ftype = argvcont.ftype & ~ FileType.LINK
    # ! Restrictions end

    recursive_text = "and subdirectories " if argvcont.recr else ""
    symlink_text   = "following symbolic links " if argvcont.follow else ""

    # ! Size functionlity
    if argvcont.size is not None:
        argvcont.ftype = FileType.FILE
        sumsize = 0
        # ? Recursive
        for dir in argvcont.walk():
            aux = 0
            for file in argvcont.match_type(dir):
                aux += file.stat().st_size
            aux = argvcont.reducesize(aux)
            if argvcont.separate:
                print(f"{argvcont.file_repr()} of {Fore.LIGHTGREEN_EX}{dir.join()}{Fore.RESET} sizes {Fore.LIGHTYELLOW_EX}{aux} {argvcont.size.value}{Fore.RESET}")
            sumsize += aux

        if argvcont.separate:
            print("")
            return 0

        if argvcont.blank:
            print(sumsize)
        elif sumsize == 0:
            print(f"No {argvcont.file_repr()} was found, they are {Fore.LIGHTRED_EX}empty{Fore.RESET} or the size is {Fore.LIGHTYELLOW_EX}too low{Fore.RESET} to show digits with this size modifier")
        elif argvcont.is_cd:
            print(f'The {argvcont.file_repr()} of {Fore.LIGHTBLUE_EX}this directory {Fore.RESET}{recursive_text}sizes {Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.size.value}{Fore.RESET} for filters: {argvcont.repr_filters()} {symlink_text}')
        else:
            print(f'The {argvcont.file_repr()} of {argvcont.repr_filters()} {recursive_text}sizes {Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.size.value}{Fore.RESET} {symlink_text}')
        return 0
    # ! First ending, with size

    # ! File count functionality
    if argvcont.separate:
        if argvcont.is_cd:
            print(f"In {Fore.LIGHTBLUE_EX}this directory{Fore.RESET} {recursive_text}there are:\n")
        elif len(argvcont) > 1: # Con directorios
            print(f"For {argvcont.repr_filters()} {recursive_text}{symlink_text}there are:\n")
    
    for dir in argvcont.walk():
        aux = 0
        for file in argvcont.match_type(dir):
            aux += 1
        sumsize += aux
        if argvcont.separate and aux > 0:
            print(f"There are {Fore.LIGHTYELLOW_EX}{aux} {argvcont.file_repr()} for {Fore.LIGHTBLUE_EX}{dir.join()}{Fore.RESET}")

    # ? if -s -> all is said
    if not argvcont.separate:
        if argvcont.blank:
            print(sumsize)
        elif sumsize == 0:
            print(f"No {argvcont.file_repr()} were found for filters {argvcont.repr_filters()} {recursive_text} {symlink_text}")
        elif argvcont.is_cd:
            print(f"In this {Fore.LIGHTBLUE_EX}directory {recursive_text}{Fore.RESET}there are {Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.file_repr()}{symlink_text} matching {argvcont.repr_filters()}")
        else:
            print(f"For filters {argvcont.repr_filters()} {recursive_text}there are {Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.file_repr()} {symlink_text}")
    # ! Second ending (without size)

if __name__ == '__main__':
    exit(main())
