import os.path

import config
import requests
from datetime import date, timedelta

from cookies import get_last_answer
from services import make_graph_path, get_costs, make_graph


def get_graph_costs_per_week(symbol, count_days=config.base_history_days):
    """ Проверяет запрос с Историей на наличие ошибки, отдает название граффа с Историей """
    answer_per_week = get_last_week_currency(symbol, count_days)
    if answer_per_week.get("error", False):
        return False
    graph_path = make_graph_path(answer_per_week, symbol)
    if os.path.exists(graph_path):
        return graph_path
    else:
        costs = get_costs(answer_per_week, symbol, count_days)
        if costs:
            make_graph(costs, currency=symbol, count_days=count_days, path=graph_path)
            return graph_path
        return False


def get_last_week_currency(symbol, count_days=config.base_history_days):
    """ Возвразает ответ на запрос об истории """
    today = date.today().strftime("%Y-%m-%d")
    days_ago = (date.today() - timedelta(days=count_days)).strftime("%Y-%m-%d")
    link_for_week = config.link_for_week.format(
        start_date=days_ago,
        end_date=today,
        base=config.base_currency,
        symbol=symbol
    )
    answer = requests.get(link_for_week)
    return answer.json()


def get_currency_today():
    """ Возвращает строку в формате <Валюта>: <Значение> или False, если в запросе есть ошибка"""
    answer = get_last_answer()
    if answer.get('error', False) and answer.get('rates', False):
        return False
    result_str = ""
    for currency, value in answer['rates'].items():
        result_str += "{}: {}\n".format(currency, round(value, 2))
    return result_str.rstrip()




