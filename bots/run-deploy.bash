#!/usr/bin/bash

cd ~/Ideas/Chelly/

if [[ -z "${VIRTUAL_ENV}" ]]; then
  source cenv/bin/activate
fi

if [ -z "$1" ]
  then
    echo "No commit message supplied"
    exit 1

else
    pip freeze > requirements.txt
    git add .
    git commit -m "$1"
    git push

fi