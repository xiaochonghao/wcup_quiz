#!/bin/bash

cat > /etc/nginx/conf.d/default.conf <<EOF
upstream backend {
    server 127.0.0.1:8001;
}
server {
    listen       80;
    server_name  localhost;

    location / {
        root /data/wcup_quiz/template/;
        index index.html;
        try_files \$uri \$uri/ /;
    }

    location ~ ^/(api|docs|admin)/ {
        uwsgi_pass backend;
        include /etc/nginx/uwsgi_params;
    }

    # cannot set as '/static/', or will conflict with front
    location /tatic/ {
        alias /usr/local/lib/python2.7/site-packages/django/contrib/admin/static/;
        autoindex on;
    }
}
EOF

uwsgi --ini /data/wcup_quiz/bin/uwsgi.ini

nginx -c /etc/nginx/nginx.conf

tail -f /data/wcup_quiz/bin/uwsgi.ini
