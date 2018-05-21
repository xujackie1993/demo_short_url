#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import requests
import config
from flask import Blueprint, request, redirect, jsonify
from flask_redis import FlaskRedis

# from short_url import redis_store, app
from short_url.number_sender import get_number
from short_url.decorator import crossdomain

short_url_api = Blueprint('short', __name__)
EXPIRE_TIME_DELTA = config.EXPIRE_TIME_DELTA
HOST = config.HOST
# redis_store = FlaskRedis(app)

@short_url_api.route('/', methods=['POST'])
@crossdomain('*')
def shorten():
    return "hello"
    url = request.form.get('url')
    short_url = redis_store.get(url)
    if short_url is None:
        short_url = get_number()
        redis_store.set(short_url, url)
        redis_store.set(url, short_url)
        if not pre_check(url):
            return jsonify({'data': "url is not accessable"})

    else:
        expire_time = datetime.now() + timedelta(seconds=EXPIRE_TIME_DELTA)
        redis_store.expireat(url, expire_time)

    if mod.url_prefix:
        rv = '{0}{1}/{2}'.format(HOST, mod.url_prefix, short_url)
    else:
        rv = '{0}/{1}'.format(HOST, short_url)
    return jsonify({'data': rv})


@short_url_api.route('/<path:url>')
def recovery_url(url):
    rv = redis_store.get(url)
    if rv is not None:
        return redirect(rv, code=302)
    else:
        return 'error'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive'
}


def pre_check(url):
    rv = False
    try:
        response = requests.get(url, headers=headers, timeout=1)
        if response.status_code == 200:
            rv = True
    except Exception as e:
        rv = False
    return rv