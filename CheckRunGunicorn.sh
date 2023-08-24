#!/bin/bash

count=$(ps aux | grep python | grep 'BookStoreServer.wsgi' | grep -v grep | grep -v kill | wc -l)

if [[ $count -ge 1 ]]; then
    exit 1
else
    exit 0
fi