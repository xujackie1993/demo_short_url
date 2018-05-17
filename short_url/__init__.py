#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import conf
import logging
import traceback
from flask_redis import FlaskRedis

app = flask.Flask("short_url", instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.secret_key = app.config['SECRET_KEY']
app.url_map.strict_slashes = False
redis_store = FlaskRedis(app)

from short_url.views import short_url_api

@app.errorhandler(Exception)
def handle_error(e):
    logger = logging.getLogger("error")
    logger.exception(e)
    if getattr(conf, 'DEBUG', False):
        resp = traceback.format_exception(type(e), e, e.__traceback__)
        print(resp)
    else:
        resp = "Things can go wrong will go wrong,"\
               + "so are servers."
    return flask.Response(response=resp, status=500)


app.register_blueprint(short_url_api, url_prefix="/short")