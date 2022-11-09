#!/usr/bin/bash

cd ~/Ideas/Chelly

if [[ -z "${VIRTUAL_ENV}" ]]; then
  source cenv/bin/activate
fi

py.test

rm -rf __pycache__