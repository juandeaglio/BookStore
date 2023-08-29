config="""server{
    listen {nginx_port};
    server_name {server_name};

    location /static/ {
        user root;
        alias {static_path}/;
    }
    location /static/imgs/ {
        user root;
        alias {static_path}/imgs/;
    }

    location / {
        proxy_pass http://localhost:{gunicorn_port};
    }
}"""