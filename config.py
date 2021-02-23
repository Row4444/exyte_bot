import os

BOT_TOKEN = os.getenv("EXYTE_TOKEN")  # Token

link = 'https://api.exchangeratesapi.io/latest?base='
link_for_week = 'https://api.exchangeratesapi.io/history?start_at={start_date}&end_at={end_date}&base={base}&symbols={symbol}'

base_currency = 'USD'

graphs_path = "graphs/"

name_last_answer_in_redis = 'last_answer'
time_to_hash_in_seconds = 600

base_history_days = 7

