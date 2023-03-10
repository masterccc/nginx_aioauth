# nginx_aioauth

Add authentication at web server level with auth_request module (https://nginx.org/en/docs/http/ngx_http_auth_request_module.html) and aiohttp.


## Nginx configuration
```

    # Require authentication to access /protected_area

    location /protected_area {
        auth_request /auth;
    }

    # Send auth data to python script
    location = /auth {
        proxy_pass               http://127.0.0.1:8080/;
        proxy_pass_request_body  off;
        proxy_set_header         Content-Length "";
        proxy_set_header         X-Original-URI $request_uri;
        proxy_pass_header        Cookie;
        proxy_set_header         Cookie $http_cookie;
    }

    # Urls that doesn't require auth
    location /login.html {}
    location /images/ {}
    location /favicon.png {}
    location /api {
        proxy_pass http://127.0.0.1:8080;
    }
```

  