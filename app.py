#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import logging
import traceback
import config
from flask_redis import FlaskRedis

app = flask.Flask("short_url")
# redis_store = FlaskRedis(app)

from short_url.views import short_url_api

@app.errorhandler(Exception)
def handle_error(e):
    logger = logging.getLogger("error")
    logger.exception(e)
    if getattr(config, 'DEBUG', False):
        resp = traceback.format_exception(type(e), e, e.__traceback__)
        print(resp)
    else:
        resp = "Things can go wrong will go wrong,"\
               + "so are servers."
    return flask.Response(response=resp, status=500)


app.register_blueprint(short_url_api, url_prefix="/short")

app.run(debug=True, host="0.0.0.0", port=8080)