# wechat-token-proxy
WeChat access-token proxy

## Prerequisite
python version >= 3.5

## Usage
run the token proxy and fetch "http://proxy-ip:80/"
```bash
curl http://localhost:80/
{"access_token":"16_FoD_IkcmZxmZ3IX4sciqaRGc3Ch3Y6nq0U-E2PfZiObUHSqGc0vMrhkm1ExkDDTewyKWaDS8qrcITCGknU4ew3wqWtLcWDeXOSVSXXzeRooApFkhjXwiGXjslD0J87S-Y5Sz7PwXjZkyqKLMIUYbABARDH","expire_in":6799}
```
refresh the token 5 minutes before it expires, the old one still works for 5 minutes

### to test
git clone this repo, then execute
```bash
$ pip install flask requests
$ cd wechat-token-proxy
$ APPID=<your APPID> APPSECRET=<your APPSECRET> python proxy.py
```

### run in production
git clone this repo, then execute
```bash
$ pip install flask requests gunicorn meinheld
$ cd wechat-token-proxy
$ APPID=<your APPID> APPSECRET=<your APPSECRET> gunicorn --bind 0.0.0.0:80 --worker-class="egg:meinheld#gunicorn_worker" --workers 1 proxy:app
```

### run with docker
git clone this repo, then execute
```bash
$ cd wechat-token-proxy
$ docker build -t wechat-token-proxy .
$ docker run -d -p 80:80 -e APPID=<your APPID> -e APPSECRET=<your APPSECRET> wechat-token-proxy
```

### add-ons

#### Flask-Limiter
git clone this repo, then execute
```bash
$ pip install flask requests gunicorn meinheld Flask-Limiter
$ cd wechat-token-proxy
$ APPID=<your APPID> APPSECRET=<your APPSECRET> RATE_LIMITS="6 per minute; 60 per hour; 600 per day" gunicorn --bind 0.0.0.0:80 --worker-class="egg:meinheld#gunicorn_worker" --workers 1 proxy:app
```

#### Sentry
git clone this repo, then execute
```bash
$ pip install flask requests gunicorn meinheld raven
$ cd wechat-token-proxy
$ APPID=<your APPID> APPSECRET=<your APPSECRET> SENTRY_DSN=<your sentry dsn> gunicorn --bind 0.0.0.0:80 --worker-class="egg:meinheld#gunicorn_worker" --workers 1 proxy:app
```
