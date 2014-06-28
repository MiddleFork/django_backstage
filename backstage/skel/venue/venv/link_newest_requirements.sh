#!/bin/sh
unlink requirements.txt
ln -s `ls -t requirements.*.txt|head -1` requirements.txt
