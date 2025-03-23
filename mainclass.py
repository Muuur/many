#1/usr/bin/python3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Self
from os import sep
from sys import stdout, stderr, argv
from itertools import chain, product, starmap
from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import Fore
from enums import *

@dataclass
class NoDir():
    """
    Main dataclass NoDir. The name is legacy, it represents a filter with a directory inside.
    
    Parameters
    ----------
    path: str
        The directory path

    filter: Optional[str] = None
        The filter to search for in the directory.
        The default is None, that means all contents (*).
    """
    path:   Path
    filter: str = '*'

    def __repr__(self) -> str:
        return f"NoDir(path={self.path}, filter={self.filter})"

    def __hash__(self) -> int:
        return hash(self.join())

    @classmethod
    def frompath(cls, nodir: Path) -> 'NoDir':
        """
        Creates a NoDir entry from a Path object
        
        Parameters
        ----------
        nodir: Path
            The Path object containing the directory and the filter
            If this variable is a directory, the filter is assumed as the default
        """
        if nodir.is_dir():
            return cls(nodir)
        return cls(
            path=nodir.parent,
            filter=nodir.name
        )
    
    def join(self) -> str:
        """
        Represents the NoDir entry as a path string
        
        Parameters
        ----------
        None
        
        Returns
        -------
        join: str
            The path representation in string format
        """
        return self.path.joinpath(self.filter).as_posix()
    
    def glob(self) -> Iterator[Path]:
        """
        Search for files in the directory self.path matching self.filter with shell expansion
        
        Parameters
        ----------
        None
        
        Returns
        -------
        glob: Iterator[Path]
            An interator over the files matching the pattern in the directory
        """
        if self.filter is None:
            yield from self.path.iterdir()
        else:
            yield from self.path.glob(self.filter)

@dataclass
class ArgvContainer():
    """
    Main dataclass ARGV container.
    Keeps the argv parameters and unify the functions.
    
    Parameters
    ----------
    ftype: FileType
        The file type that the program will recognise, default is FILE | DIR
    
    size: Size
        The file size that the program will show, default is B (bytes)

    follow: bool
        Whether follow symlink_texts or not
    
    blank: bool
        This parameter indicates that the output should only display the number and not any text

    recr: bool
        If the search show be recursive or not

    separate: bool
        If the output will be separate between filters or not
    
    round: int
        The floating point decimals to round the output, default 2
    
    filters: set[NoDir]
        The filters to search for without duplicates
    """
    ftype:    FileType
    size:     Size
    follow:   bool
    blank:    bool
    recr:     bool
    separate: bool
    round:    int  = 2
    _is_cd:   bool = False
    filters:  set[NoDir] = field(default_factory=set[NoDir])

    def __len__(self) -> int:
        return len(self.filters)
    
    def __iter__(self) -> Iterator[NoDir]:
        yield from self.filters

    @property
    def is_cd(self) -> int:
        return self._is_cd

    def repr_filters(self, sep: str=", ") -> str:
        """
        Display the filters in a prettier format

        Parameters
        ----------
        sep: str = ", "
            The string separator between filters, default a comma with a space

        Returns
        -------
        repr_filters: str
            The string representation of the filters
        """
        return f'{Fore.LIGHTBLUE_EX}{sep.join(map(NoDir.join, self.filters))}{Fore.RESET}'

    def parse(self, filters: list[str]) -> Self:
        """
        Parse the filters into directories, files and nodir.
        Then unifiy them as nodir all of them.

        Parameters
        ----------
        filters: list[str]
            The list of filters to process, the result will be the unique of all of them.
            The final length of filters will be len(dires) * len(filters) + len(nodires)
            with removed duplicates.

        Returns
        -------
        Self
        """
        dires:   list[Path]  = []
        filt:    set[str]    = set()
        nodires: list[NoDir] = []
        for f in filters:
            pth = Path(f)
            if pth.is_dir():
                dires.append(pth)
            elif sep in f:
                nodires.append(NoDir.frompath(pth))
            else:
                filt.add(f)

        if len(nodires) == 0:
            if len(dires) == 0:
                dires.append(Path())
                self._is_cd = True
            if len(filt) == 0:
                if self.separate and not self.recr:
                    filt.update(f"*{file.suffix}" for file in chain(*map(Path.iterdir, dires)) if self.issth("is_file", file))
                else:
                    filt.add("*")
        elif len(dires) == 0:
            if len(filt) > 0:
                filt.clear()
        elif len(filt) == 0:
            filt.add("*")

        nodires.extend(starmap(NoDir, product(dires, filt)))
        self.filters = set(nodires) if len(nodires) > 0 else {NoDir(Path())}
        return self

    def match_type(self, dir: NoDir) -> Iterator[Path]:
        """
        Search for the files in the direcotry associated with the corresponding filter
        
        Parameters
        ----------
        dir: NoDir
            The NoDir object that contains the files
        
        Returns
        -------
        match_type: Iterator[Path]
            An iterator over the resulting files choosing the ones that match the requirements
        """
        for file in dir.glob():
            if file.is_symlink():
                if self.ftype & FileType.LINK == FileType.LINK:
                    yield file
                elif not self.follow:
                    continue
            if (self.ftype & FileType.FILE and file.is_file()) or \
                (self.ftype & FileType.DIR and file.is_dir()) or \
                (self.ftype & FileType.FIFO and file.is_fifo()) or \
                (self.ftype & FileType.CHAR and file.is_char_device()) or \
                (self.ftype & FileType.BLOCK and file.is_block_device()) or \
                (self.ftype & FileType.SOCKET and file.is_socket()):
                yield file

    def file_repr(self) -> str:
        """
        Display chosen file types on screen

        Parameters
        ----------
        None

        Returns
        -------
        file_repr: str
            The string representation of chosen file types
        """
        repr = ""
        if self.ftype & FileType.FILE:
            repr += "files, "
        if self.ftype & FileType.DIR:
            repr += "directories, "
        if self.ftype & FileType.LINK and not self.follow:
            repr += "links, "
        if self.ftype & FileType.CHAR:
            repr += "char devices, "
        if self.ftype & FileType.BLOCK:
            repr += "block devices, "
        if self.ftype & FileType.FIFO:
            repr += "fifos, "
        if self.ftype & FileType.SOCKET:
            repr += "socket, "
        return f'{Fore.LIGHTGREEN_EX}{repr[:-2]}{Fore.RESET}'

    def walk(self) -> Iterator[NoDir]:
        """
        Wrapper for os.walk of a NoDir entry
        
        Parameters
        ----------
        None

        Returns
        -------
        walk: Iterator[NoDir]
            Iterates over all files and directories recurvisely (or not) over the tree
            This function won't operate recursively if the recr flag is not set
        """
        if self.recr:
            ddires = list(self.filters)[::-1]
            while len(ddires) > 0:
                last = ddires.pop()
                yield last
                try:
                    tmp = [NoDir(i, last.filter) for i in last.path.iterdir() if self.issth("is_dir", i)]
                    if len(tmp) > 0:
                        tmp.reverse()
                        ddires.extend(tmp)
                except PermissionError as prm:
                    ArgvContainer.print_permission(prm)
        else:
            yield from self.filters

    def issth(self, sth: str, test: Path) -> bool:
        """
        Test if the file is of a certain type and not a symlink_text, or is a symlink_text while follow flag is set

        Parameters
        ----------
        sth: str
            The file type to test
        
        test: Path
            The file to test type
        """
        return getattr(test, sth)() and (not test.is_symlink() or (self.follow and test.is_symlink()))

    def reducesize(self, num: float) -> float:
        """
        Converts the size into the size specified as parameter, default no conversion
        
        Parameters
        ----------
        num: float
            The number to convert

        Returns
        -------
        reducesize: float
            The number converted into other unit
        """
        match self.size:
            case Size.KB:
                res = num / 2**10
            case Size.MB:
                res = num / 2**20
            case Size.GB:
                res = num / 2**30
            case Size.TB:
                res = num / 2**40
            case _:
                res = num
        return round(res, self.round)

    @staticmethod
    def print_permission(perror: PermissionError) -> None:
        """
        Default PermissionError handler

        Parameters
        ----------
        perror: PermissionError
            The permission error object

        Returns
        -------
        None
        """
        print(f"many: {Fore.LIGHTRED_EX}error{Fore.RESET} at reading {Fore.LIGHTBLUE_EX}{perror.filename}{Fore.RESET} -> {Fore.LIGHTYELLOW_EX}permission error{Fore.RESET}", file=stderr)

    @classmethod
    def parse_args(cls, args: list[str]=argv[1:]) -> 'ArgvContainer':
        """
        Parse the console arguments into a ArgvContainer object
        This function creates the argparse.ArgumentParser object and parses argv

        Parameters
        ----------
        args: list[str] = argv[1:]
            The arguments to parse, default argv ignoring argv[0]
        
        Returns
        -------
        parse_args: ArgvContainer
            The ArgvContainer object for the application
        """
        bold, under, reset = ("\x1b[1m", "\x1b[4m", "\x1b[0m") if stdout.isatty() else ("", "", "")

        parser = ArgumentParser(
            description="Show how many regular or special files or folders are in directories, or show file size",
            epilog=f"""Tips:
				You can filter using glob shell expansion rules (like {'~/Pictures/\\*.png' if sep == '/' else 'D:/images/*.jpg'.replace("/", sep)})
				Filters should be {under}escaped{reset} with -r or -s, because the program may fail
				,it is optimized to perform with escaped filters, and the output will be cleaner

				{bold}Colors{reset}:
				    Blue indicates directories and/or filteres
				    Green indicates file types
				    Yellow indicates figures
				    Red indicates errors
				    Magenta indicates warnings

				{bold}Warnings{reset}:
				    With -ykmgbt (size), the parameters -adlcbFS (file type) are ignored
				    -R (size round) is ignored without -ykmgbt (size)
				    -l (search links) is ignored with -f (follow links)
				    Default filter is -ad (files and directories)
                    Default floating point round is 2

				{bold}Restrictions{reset}:
				    You must specify at least two filters to use -s, or use it with -r
				    You cannot separate with blank output, -s is incompatible with -n
                
				{bold}Filter types{reset}
				    Filters are firstly divided into three categories: filters, directories and NoDir
				    A NoDir entry is a directory followed by a filter in the same parameter.
				    The filters are classified using the following criteria:
				        If the directory exists, then is a directory
				        Elif the entry has directory separators inside, then is NoDir
				        Else, a filter
				    All the directories and filters are converted into NoDir entries by cartesian product
				    and then putting them together with the rest of original NoDir entries.
				    For example, /home/$USER /media/$USER /usr/bin/python* '*.pdf' '*.mp4' gives:
				        /home/$USER/*.pdf
				        /home/$USER/*.mp4
				        /media/$USER/*.pdf
				        /media/$USER/*.mp4
				        /usr/bin/python*
				    Default is ./*""".replace('\t', ''),
            formatter_class=RawTextHelpFormatter
        )
        parser.add_argument("-a", "--files", action="store_const", default=0, const=FileType.FILE, help=f"Filter {under}files{reset}", dest="files")
        parser.add_argument("-d", "--dir", action="store_const", default=0, const=FileType.DIR, help=f"Filter {under}directories{reset}", dest="dires")
        parser.add_argument("-l", "--links", action="store_const", default=0, const=FileType.LINK, help=f"Filter {under}symbolic links{reset}", dest="links")
        parser.add_argument("-c", "--char", action="store_const", default=0, const=FileType.CHAR, help=f"Filter {under}char devices{reset}", dest="chardev")
        parser.add_argument("-b", "--block", action="store_const", default=0, const=FileType.BLOCK, help=f"Filter {under}block devices{reset}", dest="blockdev")
        parser.add_argument("-F", "--fifo", action="store_const", default=0, const=FileType.FIFO, help=f"Filter {under}fifo{reset} files", dest="fifo")
        parser.add_argument("-S", "--socket", action="store_const", default=0, const=FileType.SOCKET, help=f"Filter {under}socket{reset} files", dest="socket")

        parser.add_argument("-f", "--follow", action="store_true", help="Follow symbolic links", dest="follow")
        parser.add_argument("-n", "--blank", action="store_true", help="Brief output, show only the number, made for $(subprocess substitution) in scripts", dest="blank")
        parser.add_argument("-r", "--recursive", action="store_true", help="Iterate recursively over directories", dest="recursive")
        parser.add_argument("-s", "--separate", action="store_true", help="Separate over the filters. With no filters search for all extensions", dest="sep")

        parser.add_argument("-y", "--size", action="store_const", dest="size", const=Size.B, help="Display size instead of file count. Size in B")
        parser.add_argument("-k", "--kb", action="store_const", dest="size", const=Size.KB, help="Display size instead of file count. Size in KB")
        parser.add_argument("-m", "--mb", action="store_const", dest="size", const=Size.MB, help="Display size instead of file count. Size in MB")
        parser.add_argument("-g", "--gb", action="store_const", dest="size", const=Size.GB, help="Display size instead of file count. Size in GB")
        parser.add_argument("-t", "--tb", action="store_const", dest="size", const=Size.TB, help="Display size instead of file count. Size in TB")
        
        parser.add_argument("-R", "--round", type=int, dest="round", help="Decimal round", required=False, default=2)

        parser.add_argument("filters", nargs='*', help="File filters or directories to apply, default all files")

        parser.add_argument("-v", "--version", action="version", version="6.0")
        # parser.add_argument("-h", "-?", "--help", action="help")

        argparse = parser.parse_args(args)
        ftype = argparse.files | argparse.dires | argparse.links | argparse.chardev | argparse.blockdev | argparse.fifo | argparse.socket \
            or FileType.FILE | FileType.DIR
        return cls(
            follow=argparse.follow,
            ftype=ftype,
            size=argparse.size,
            blank=argparse.blank,
            recr=argparse.recursive,
            separate=argparse.sep,
            round=argparse.round
        ).parse(argparse.filters)

__all__ = ["ArgvContainer", "NoDir"]
