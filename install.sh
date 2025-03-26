#!/usr/bin/bash
pyver="$(pip -V | grep -Po 'python\d\.\d+')"

if (( $(id -u) == 0 ))
then
    root=/usr/local
    pyroot=$root/lib/$pyver/dist-packages
else
    root=$HOME/.local
    pyroot=$root/lib/$pyver/site-packages
fi
distdir=$pyroot/many-6.2.0-dist-info
manydir=$pyroot/many

mkdir -p $manydir $distdir
pip install -r requirements.txt
cp *.py $manydir
cp README.md LICENSE $distdir
ln -s $pyroot/many/__main__.py $root/bin/many
