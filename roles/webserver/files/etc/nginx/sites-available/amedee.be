# Rate Limiting
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

# Server Block for HTTPS
server {
    root /var/www/html;
    index index.php;
    server_name amedee.be;

    location / {
        limit_req zone=mylimit burst=20 nodelay;
        try_files $uri $uri/ /index.php?q=$uri&$args /index.php$is_args$args /index.php?$query_string =404;
    }

    # PHP Processing
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    # Restrict Access to Hidden Files
    location ~ /\.ht {
        deny all;
    }

    # Logging Configurations
    location = /favicon.ico { log_not_found off; access_log off; }
    location = /robots.txt { log_not_found off; access_log off; allow all; }

    # Static Files Caching
    location ~* \.(css|gif|ico|jpeg|jpg|js|png|svg|woff|woff2|eot|ttf|otf)$ {
        expires 30d;
        add_header Cache-Control "public";
        log_not_found off;
        try_files $uri =404;
    }

    # Deny Access to .user.ini
    location ~ ^/\.user\.ini {
        deny all;
    }

    # JetPack IP Whitelisting for xmlrpc.php
    location = /xmlrpc.php {
        error_page 403 = @xmlrpc;
        allow 192.0.64.0/18;
        allow 64.34.206.0/24;
        allow 198.181.116.0/22;
        allow 66.155.105.128/26;
        allow 69.90.253.0/24;
        allow 76.74.248.128/25;
        allow 76.74.255.0/25;
        allow 2001:1978:1e00:3::/64;
        allow 2620:115:c000::/40;
        deny all;
    }
    location @xmlrpc {
        return 301 https://$host/xmlrpc/;
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

    # Improve Security Headers
    add_header Content-Security-Policy "default-src 'self'";
    add_header Feature-Policy "geolocation 'self'";
    add_header Permissions-Policy "geolocation=(self)";
    add_header Referrer-Policy no-referrer-when-downgrade;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

}

# Redirect all HTTP traffic to HTTPS
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    server_tokens off;

    location / {
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        return 301 https://amedee.be$request_uri;
    }
}
