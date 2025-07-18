# Rate Limiting
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

# Server Block for HTTPS
server {
    root /var/www/html;
    index index.php;
    server_name amedee.be;

    add_header Cache-Control "public, max-age=31536000, immutable";

    location / {
        limit_req zone=mylimit burst=20 nodelay;
        try_files $uri $uri/ /index.php?q=$uri&$args;
    }

    # PHP Processing
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    # Restrict Access to Hidden Files
    location ~ /\.ht {
        deny all;
    }

    # Logging Configurations
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }
#     location = /robots.txt {
#         access_log off;
#         allow all;
#         log_not_found off;
#         try_files $uri /?robots=1;
#     }

    # Static Files Caching
    location ~* \.(css|gif|ico|jpeg|jpg|js|png|svg|woff|woff2|eot|ttf|otf)$ {
        expires 1y;
        log_not_found off;
        try_files $uri =404;
    }

    # Deny Access to .user.ini
    location ~ ^/\.user\.ini {
        deny all;
    }

    # Disable Unwanted HTTP Requests
    if ($request_method !~ ^(GET|HEAD|POST)$) {
        return 444;
    }

    # SSL Configuration
    listen 443 ssl; # managed by Certbot
    listen [::]:443 ssl;
    ssl_certificate /etc/letsencrypt/live/amedee.be/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/amedee.be/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

# Redirect all HTTP traffic to HTTPS
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    server_tokens off;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        return 301 https://amedee.be$request_uri;
    }
}
