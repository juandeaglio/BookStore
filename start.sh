#/bin/bash
gunicorn -b 0.0.0.0:8091 BookStoreServer.wsgi &
nginx -g 'daemon off;'