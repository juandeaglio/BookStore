#!/bin/bash

count=$(ps aux | grep python | egrep 'runserver|gunicorn' | grep -v grep | wc -l)

if [[ $count -ge 1 ]]; then
    exit 1
else
    exit 0
fi