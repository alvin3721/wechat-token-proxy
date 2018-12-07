#! /usr/bin/env python3

import unittest

import requests

from proxy import app


class WeChatTokenProxyTestCase(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):

        pass

    def test_access_token(self):

        rv = self.client.get('/')
        data = rv.get_json()
        assert data['expire_in'] > 0
        assert data['access_token'] is not None
        requests.get(
            'https://api.weixin.qq.com/cgi-bin/getcallbackip',
            params={'access_token': data['access_token']}
        )
        resp = requests.get(
            'https://api.weixin.qq.com/cgi-bin/getcallbackip',
            params={'access_token': data['access_token']}
        )
        assert resp.status_code == 200
        resp_data = resp.json()
        assert resp_data.get('errcode') in (None, 0)


def suit():

    suit = unittest.TestSuite()
    suit.addTest(WeChatTokenProxyTestCase('test_access_token'))

    return suit


if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(suit())
