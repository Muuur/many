# Many

This program search and count for files or file sizes in a specified directories using glob filters.

Muuur - 2020

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
# Count all things in current directory
many

# Count pdf files stored in bar folder and files starting with a in baz folder
many -a 'bar/*.pdf' 'baz/a*'

# Get help
many --help

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
