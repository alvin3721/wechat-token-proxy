#! /usr/bin/env python3

import logging
import os
import threading
import time

import requests
from flask import Flask, jsonify


class AccessToken:
    """Fetch WeChat access_token"""

    token_url = 'https://api.weixin.qq.com/cgi-bin/token'

    def __init__(self, appid, appsecret, logger, threshold=300):

        self.appid = appid
        self.appsecret = appsecret
        self.logger = logger
        self.threshold = threshold
        self.lock = threading.Lock()
        self.access_token = None
        self.expire_at = 0

    def trigger(self):
        """return True when the update condition is met"""

        return self.expire_at - time.time() < self.threshold

    def __call__(self):

        # Refresh the access_token ${threshold} seconds before it expires,
        # after refreshing, the old one works still for 5 minutes
        if self.trigger() and self.lock.acquire() and self.trigger():
            payload = {
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.appsecret
            }
            try:
                # fetch access_token
                resp = requests.get(
                    self.token_url,
                    params=payload
                )
                data = resp.json()
                assert data.get('errcode', 0) == 0
            except Exception as exc:
                self.logger.error('Failed to fetch access_token!')
                self.lock.release()
                raise exc
            else:
                # update local cache
                self.expire_at = time.time() + data['expires_in']
                self.access_token = data['access_token']
                self.logger.info(
                    'new access_token: %s' % data['access_token']
                )
        if self.lock.locked():
            self.lock.release()

        return {
            'access_token': self.access_token,
            'expire_in': int(self.expire_at - time.time())
        }


# AppId and AppSecret
appid = os.environ['APPID'].strip()
appsecret = os.environ['APPSECRET'].strip()

# Rate Limits
rate_limits = os.environ.get('RATE_LIMITS')

# Sentry
sentry_dsn = os.environ.get('SENTRY_DSN')


def create_app():

    app = Flask(__name__)

    # Sentry
    if sentry_dsn:
        from raven.contrib.flask import Sentry
        sentry = Sentry(app, dsn=sentry_dsn.strip())
        sentry.init_app(app)

    # Flask-Limiter
    if rate_limits:
        from flask_limiter import Limiter
        from flask_limiter.util import get_ipaddr
        limiter = Limiter(
            key_func=get_ipaddr,
            default_limits=list(filter(
                lambda rule: rule.strip() != '',
                rate_limits.split(';'))
            )
        )
        limiter.init_app(app)

    return app


app = create_app()
app.logger.setLevel(logging.INFO)

access_token = AccessToken(appid, appsecret, app.logger)


@app.route('/')
def get_access_token():

    return jsonify(access_token())


if __name__ == '__main__':

    app.run('0.0.0.0', 8080, debug=True, threaded=True, processes=1)
