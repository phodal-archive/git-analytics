#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["get_connection", "get_pipeline", "format_key"]

import redis
redis_pool = None
DEFAULT_TTL = 6 * 30 * 24 * 60 * 60

def get_connection():
    global redis_pool
    if redis_pool is None:
        redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    return redis.Redis(connection_pool=redis_pool)


def get_pipeline():
    r = get_connection()
    return r.pipeline()


def format_key(key):
    return "{0}:{1}".format("commit", key)

def redis_execute(pipe, cmd, key, *args, **kwargs):
    key = format_key(key)
    r = getattr(pipe, cmd)(key, *args, **kwargs)
    pipe.expire(key, DEFAULT_TTL)
    return r