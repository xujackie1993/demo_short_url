#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from short_url import redis_store
from short_url.number_convert import _10_to_62
from short_url import redis_store

REDIS_KEY = "NUMBER_SENDER"

def get_number():
    return str(_10_to_62(redis_store.incr(REDIS_KEY)))
