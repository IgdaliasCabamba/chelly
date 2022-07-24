#!/usr/bin/bash

cd ~/Ideas/Chelly/

if [ -z "$1" ]
  then
    echo "No commit message supplied"
    exit 1

else

    git add .
    git commit -m "$1"
    git push

fi