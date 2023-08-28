config="""server{
    listen {nginx_port};
    server_name {server_name};

    location /static/ {
        alias {static_path}/;
    }
    location /static/imgs/ {
        alias {static_path}/imgs/;
    }

    location / {
        proxy_pass http://localhost:{gunicorn_port};
    }
}"""