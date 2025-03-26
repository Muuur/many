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
from enums import FileType
from mainclass import ArgvContainer

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
    print(
        sub(r'^ *', '', msg),
        f"Please run `{Path(argv[0]).name} --help` to get help",
        file=stderr,
        sep="\n\n"
    )
    exit(code)

def main(argv: list[str]=argv) -> int:
    """
    Main function, it performs all of the operations to count files or get file sizes
    
    Parameters
    ----------
    argv: list[str] = argv
        Console arguments, default sys.argv

    Returns
    -------
    main: int
        Status code, 0 if die was not called
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
    if argvcont.separate:
        if argvcont.blank:
            die(f"many: You {Fore.RED}cannot{Fore.RESET} separate output and run it blank, -s is incompatible with -n")
        elif not argvcont.recr and len(argvcont) < 2:
            die(f"You can't separate output with less than 2 filters or without recursive flag")
    elif argvcont.separate and (not argvcont.recr and len(argvcont) == 1):
        die(f"many: You {Fore.RED}must specify{Fore.RED} -r or at least two {Fore.LIGHTGREEN_EX}filters{Fore.RESET} to use -s")
    # elif argvcont.ftype & FileType.LINK and argvcont.follow:
    #     print(f"many: {Fore.LIGHTMAGENTA_EX}warning{Fore.RESET} you {Fore.RED}can't{Fore.RESET} count symbolic links while follow them, -l is {Fore.RED}incompatible{Fore.RESET} with -f", file=stderr)
    #     argvcont.ftype = argvcont.ftype & ~ FileType.LINK
    elif argvcont.size is not None and argvcont.ftype & ~ (FileType.FILE | FileType.DIR) != 0:
        print(f"many: {Fore.LIGHTMAGENTA_EX}warning{Fore.RESET}: any file type filter like directory will be {Fore.RED}ignored{Fore.RESET} while counting size")
        argvcont.ftype = FileType.FILE
    # ! Restrictions end

    recursive_text = "and subdirectories " if argvcont.recr else ""
    symlink_text   = "following symbolic links " if argvcont.follow else ""
    recprint       = False

    # ! Size functionlity
    if argvcont.size is not None:
        argvcont.ftype = FileType.FILE
        sumsize = 0

        # ? Recursive
        for filter in argvcont:
            for dir in filter.walk(argvcont.recr, argvcont.follow):
                aux = sum(
                    file.stat(follow_symlinks=argvcont.follow).st_size \
                    for file in dir.glob(filter.filter)     
                    if argvcont.match_type(file)
                )
                sumsize += aux
                if argvcont.separate and aux > 0:
                    recprint = True
                    print(f"{Fore.LIGHTYELLOW_EX}{argvcont.reducesize(aux)} {argvcont.size.value}{Fore.RESET} {argvcont.file_repr()} of {Fore.LIGHTGREEN_EX}{dir}/{filter.filter}{Fore.RESET}")

        sumsize = argvcont.reducesize(sumsize)
        if not argvcont.separate and not recprint:
            if argvcont.blank:
                print(sumsize)
            elif argvcont.is_cd:
                print(f'{Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.size.value}{Fore.RESET} {argvcont.file_repr()} {symlink_text}in {Fore.LIGHTBLUE_EX}this directory {Fore.RESET}{recursive_text}matching {argvcont.repr_filters()}')
            else:
                print(f'{Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.size.value}{Fore.RESET} {argvcont.file_repr()} {recursive_text}{symlink_text}matching {argvcont.repr_filters()}')
        # ! First ending, with size
    else:
        # ! File count functionality
        for filter in argvcont:
            for dir in filter.walk(argvcont.recr, argvcont.follow):
                aux = sum(1 for file in dir.glob(filter.filter) if argvcont.match_type(file))
                sumsize += aux
                if argvcont.separate and aux > 0:
                    recprint = True
                    print(f"{Fore.LIGHTYELLOW_EX}{aux} {argvcont.file_repr()} matching {Fore.LIGHTBLUE_EX}{dir}/{filter.filter}{Fore.RESET}")

        # ? if -s -> all is said
        if not argvcont.separate and not recprint:
            if argvcont.blank:
                print(sumsize)
            elif argvcont.is_cd:
                print(f"{Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.file_repr()} {symlink_text}in this {Fore.LIGHTBLUE_EX}directory {Fore.RESET}{recursive_text}matching {argvcont.repr_filters()}")
            else:
                print(f"{Fore.LIGHTYELLOW_EX}{sumsize} {argvcont.repr_filters()} {recursive_text}{symlink_text}matching {argvcont.file_repr()}")
    # ! Second ending (without size)

    return 0

if __name__ == '__main__':
    exit(main())
