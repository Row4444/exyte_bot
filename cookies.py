import json
import redis
import requests

import config

r = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
)


def get_answer():
    return requests.get(config.link + config.base_currency).text


def set_new_answer():
    """ Заносим новые значения валют в Redis с таймером и возвращает его в формате json """
    answer = get_answer()
    r.set(config.name_last_answer_in_redis, answer)
    r.expire(config.name_last_answer_in_redis, config.time_to_hash_in_seconds)
    return json.loads(answer)


def get_last_answer():
    """ Берет последние значения курсов из базы и возвращает их """
    last_answer_b = r.get(config.name_last_answer_in_redis)
    if last_answer_b:
        last_answer = last_answer_b.decode("utf-8")
        last_answer_json = json.loads(last_answer)
    else:
        last_answer_json = set_new_answer()
    return last_answer_json
