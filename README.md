# Many 6.2

This program search and count how many files, or file sizes there are in specified directories with glob filters

---

Muuur - 2020

---

## Getting the package

```bash
# Get the repository
git clone https://github.com/Muuur/many
cd many
```

## Installing the package

```bash
# With bash
bash install.sh

# Or
./install.sh
```

# How to execute

```bash
# Get help
many -h

# Count all things in current directory
many

# Count files in directory 'foo'
many -a foo

# Count block devices recursively in '/dev' with numeric output
many -nbs /dev
```

## Filter processing

Any positional argument will be treated as a filter, they are primary differenced into 3 types:

1. Directories: if os.isdir(filter), then is treated as a directory.

2. NoDir entry: elif '/' in filter, then is a NoDir entry, it will be explained then.

3. filter: else, if the filter is not from above categories, it will be treated as file filter

Then, al entries will be converted into NoDir entries, a NoDir entry is a directory path followed by a glob filter.
So, the directories will be mixed with filters with itertools.permutations function to create all NoDir entries.
Then, the NoDir themselves will be added to filter list.
For example, positional arguments `foo bar baz/*.mp3 *.pdf a*` will generate the following NoDir entries: `foo/*.pdf foo/a* bar/*.mp3 bar/a* baz/*.mp3`

## program help

```text
usage: many [-h] [-a] [-d] [-l] [-c] [-b] [-F] [-S] [-f] [-n] [-r] [-s] [-y] [-k] [-m] [-g] [-t] [-u] [-R ROUND] [-v] [filters ...]

Show how many regular or special files or folders are in directories, or show file size

positional arguments:
  filters               File filters or directories to apply, default all files

options:
  -h, --help            show this help message and exit
  -a, --files           Filter files
  -d, --dir             Filter directories
  -l, --links           Filter symbolic links
  -c, --char            Filter char devices
  -b, --block           Filter block devices
  -F, --fifo            Filter fifo files
  -S, --socket          Filter socket files
  -f, --follow          Follow symbolic links
  -n, --blank           Brief output, show only the number, made for $(subprocess substitution) in scripts
  -r, --recursive       Iterate recursively over directories
  -s, --separate        Separate over the filters. With no filters search for all extensions
  -y, --bytes           Display size instead of file count. Size in B
  -k, --kb              Display size instead of file count. Size in KB
  -m, --mb              Display size instead of file count. Size in MB
  -g, --gb              Display size instead of file count. Size in GB
  -t, --tb              Display size instead of file count. Size in TB
  -u, --auto            Display size instead of file count. Size is computed automatically
  -R ROUND, --round ROUND
                        Decimal round
  -v, --version         show program's version number and exit

Tips:
You can filter using glob shell expansion rules (like ~/Pictures/\*.png)
Filters should be escaped with -r or -s, the program may fail because
it is optimized to run with shell-escaped glob filters, the output will be more readable also

Colors:
    - Blue for directory and/or filter names
    - Green for file types
    - Yellow for figures
    - Red for errors
    - Magenta for warnings

Warnings:
    - -ykmgbt (size) ignore the parameters -adlcbFS (file type)
    - -R (size round) is ignored without -ykmgbt (size)
    - Default file type filter is -ad (files and directories) for counting,
      and -a (files) for size count.
    - Default floating point round is 2.

Restrictions:
    - You must specify at least two filters to use -s, or use it with -r
    - You cannot separate with blank output, -s is incompatible with -n

Filter types
    - Filters are firstly divided into three categories: filters, directories and NoDir
    - A NoDir entry is a directory followed by a filter in the same parameter.
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
    Default is ./*
```

## Version history

```text
1.0   -> Show files and/or directories, parameters -ads, classify between dirs and filters
1.1   -> parameter uptake is now order free, -n added
1.5   -> -r added, minor bug fixes and new restrictions
2.0   -> -ymbgt added qith -R, some restrictions are now warnings
2.0.1 -> system quoting bug fixed
2.2   -> -r is now compatible without filters, it takes all file extensions from given directories
2.3   -> -s is now comptaiblewith -r
2.4   -> -h option added
2.5   -> -r now can take various directories
2.6   -> Dir errors fixed, UNC paths added and symlink_texts
3.0   -> Element adaptation along modificators
3.1   -> -l added and -h help bug fixed (if more parameters were given), -A:* changed to -adl
3.2   -> Quoting with space bug fixed. -st bug fixed
3.3   -> -r with no directories nor filters bug was fixed
3.4   -> NoDir added. All dires are now NoDir
3.5   -> NoDir finished
3.6   -> True-False added. -t various dires bug fixed
3.6.1 -> For bug fixed
3.6.2 -> Paths are now posix-compatible
3.7   -> Added versión (-v) and minor bug fixes
3.8   -> foreach changed to -t to admit file types, but the searches are more restrictive
3.8.1 -> Size bug fixed
3.8.2 -> nodir bug fixed
4.0   -> Changed to python and -t uptake, -h removed
4.0.1 -> -s bug fixed and another minor bugs
5.0   -> Improved eficiency with scandir
5.1   -> nodir -s fixed, el -s with size modifier and aux final instead of sumsize, inside generator bug and -r both fixed
5.2   -> PermisionError gives zero
5.2.1 -> Round added
5.2.2 -> TypeHint added
5.3   -> Colorama + PermissionError fixed + new style without files
5.4   -> Help improved, -b deleted and -n stylized, minor changes in parameter parsing
5.4.1 -> Newline bug corrected + -0 bug corrected
5.5   -> get_all_dires modification aiming eficiency + symlink_text uptake change
5.5.1 -> Another nodir bug fixed (here we go again)
5.6.2 -> Permission bug
6.0   -> All changed to classes.
         Redundancy was deleted, dires, filters and nodires were unified.
         Changed string to Path and argv parsing to argparse.ArgumentParser.
6.1   -> Added docstrings
6.2   -> Removed a bug with -s.
         Removed automatic extension search without filters for -s, now -s only works for directories, not filters.
         Removed -fl warning, now behaves as expected.
         Added auto size.
```
