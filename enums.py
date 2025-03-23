#!/usr/bin/python3
from enum import Enum, IntFlag

class FileType(IntFlag):
    """
    File type IntFlag.
    This flag aims to represent the file types that will the program search for
    """
    FILE   = 1
    DIR    = 1 << 1
    LINK   = 1 << 2
    CHAR   = 1 << 3
    BLOCK  = 1 << 4
    FIFO   = 1 << 5
    SOCKET = 1 << 6

class Size(Enum):
    """
    Size enum.
    This enum aims to represent the file size output
    """
    B  = "B"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"

__all__ = ["FileType", "Size"]
