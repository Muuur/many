# Many

This program search and count files or file sizes in directories with filters

---

Muuur - 2020

---

##Version history

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
6.0   -> All changed to classes. Redundancy was deleted. Dires, filters and nodires were unified. Changed string to Path. Changed argv parsing to argparse.ArgumentParser.
6.1   -> Added docstrings
