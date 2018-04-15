#!/bin/bash
files=pyinfog/infogs/*
export PYTHONPATH=`pwd`:$PYTHONPATH
for infog in $files
do
	if [ -f "$infog/example.py" ]; then
		python3 $infog/example.py
	fi
done


python3 pyinfog/examples/gallery/example_gallery.py
