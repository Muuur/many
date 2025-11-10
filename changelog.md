# Many Version History

### 1.0 File count

Show files and/or directories, parameters -ads, classify between dirs and filters

- 1.1    parameter uptake is now order free, -n added
- 1.2    -r added, minor bug fixes and new restrictions

### 2.0 Parameters

New parameters -ymbgt added with -r, some restrictions are now warnings

- 2.0.1  system quoting bug fixed
- 2.1    -r is now compatible without filters, it takes all file extensions from given directories
- 2.2    -s is now compatible with -r
- 2.3    Parameter -h added
- 2.4    -r now can take various directories
- 2.5    Dir errors fixed, UNC paths added and symlink_texts

### 3.0 Attributes

Element adaptation along modificators (-A:) Windows-only

- 3.1    -l added and -h help bug fixed (if more parameters were given), -A:* changed to -adl
- 3.2    Quoting with space bug fixed. -st bug fixed
- 3.3    -r with no directories nor filters bug was fixed
- 3.4    NoDir added. All dires are now NoDir (temporary)
- 3.5    NoDir finished
- 3.6    True-False added. -t various dires bug fixed
- 3.6.1  For bug fixed
- 3.6.2  Paths are now posix-compatible
- 3.7    Added versión (-v) and minor bug fixes
- 3.8    foreach changed to -t to admit file types, but the searches are more restrictive
- 3.8.1  Size bug fixed
- 3.8.2  nodir bug fixed

### 4.0 - Python

Translated into python, -t flag added, -h changed to help

- 4.0.1  -s bug fixed and another minor bugs

### 5.0 os.scandir

Improved efficiency with scandir (breaks previous version)

- 5.1    nodir -s fixed, el -s with size modifier and aux final instead of sumsize, inside generator bug and -r both fixed
- 5.2    PermisionError gives zero
- 5.2.1  Round added
- 5.2.2  TypeHints added
- 5.3    Colorama bug + PermissionError bug both fixed. New style without files
- 5.4    Help message improved, parameter -b deleted, parameter -n stylized.
         Minor changes in argv parsing
- 5.4.1  Newline bug corrected + -0 bug corrected
- 5.5    get_all_dires improves efficiency. Symlink_text parse change
- 5.5.1  Another nodir bug fixed (here we go again)
- 5.6.2  Permission bug fixed (now escape)

### 6.0 class

All program functionality changed code to classes.
Redundancy was deleted, dires, filters and nodires were unified.
Changed string to Path and argv parsing to argparse.ArgumentParser.

- 6.1    Added docstrings
- 6.2    Removed a bug with -s.
         Removed automatic extension search without filters for -s, now -s only works for directories, not filters.
         Removed -fl warning, now behaves as expected.
         Added auto size.
- 6.2.1  Corrected a bug with -s and '.', new changelog.md, fixed static type bugs (mypy)
- 6.3    Changed recursive into something similar to du, corrected a bug with -r and without recursive
- 6.4    Now the -r avoid recursive separating, it separates over argv parameters
