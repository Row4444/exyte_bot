import config

import matplotlib.pyplot as plt
from datetime import timedelta, date

fig, ax = plt.subplots()


def get_costs(answer_per_week, symbol, count_days):
    """ Составляет массив из значений запроса Истории, если даты нет, берет с предыдущего дня """
    dates = [(date.today() - timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(count_days)]
    costs = []
    default_costs = 0
    for i in reversed(dates):
        try:
            cost = answer_per_week["rates"][i][symbol]
            default_costs = cost  # (int(cost * 100)) / 100
        except KeyError:
            if not default_costs:
                continue
        costs.append(default_costs)
    if len(costs) <= 1:
        return False
    return costs


def make_graph_path(answer_per_week, currency):
    """ Генерирует имя Граффу """
    start_date = answer_per_week.get('start_at')
    end_date = answer_per_week.get('end_at')
    return '{path}{start_date}-{end_date}-{currency}.{format}'. \
        format(path=config.graphs_path, start_date=start_date, end_date=end_date, currency=currency, format="png")


def make_graph(costs, currency, count_days, path='default'):
    """ Риссует и сохраняет графф """
    plt.title("{} per {} days".format(currency, count_days))
    x = [i * -1 for i in range(len(costs), 0, -1)]
    ax.plot(x, costs)
    ax.grid(True)
    fig.savefig(path)
    plt.cla()
