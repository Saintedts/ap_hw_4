import os
import requests
from datetime import datetime
from fastapi import FastAPI
import redis


app = FastAPI()
redisio = redis.Redis(host='redis', port=6379)


def query_coins():
        currencies = dict()
        result = requests.get('https://open.er-api.com/v6/latest/USD').json()
        currencies['USD'] = result['rates']['RUB']
        result = requests.get('https://open.er-api.com/v6/latest/EUR').json()
        currencies['EUR'] = result['rates']['RUB']
        result = requests.get('https://open.er-api.com/v6/latest/CNY').json()
        currencies['CNY'] = result['rates']['RUB']
        result = requests.get('https://open.er-api.com/v6/latest/ILS').json()
        currencies['ILS'] = result['rates']['RUB']
        return currencies


@app.get("/")
def read_root():
    message = 'We work with the following currencies: USD, EUR, CNY, ILS'
    return {"message": message}


@app.get("/get_currencies")
def get_currencies():
    if redisio.exists("currencies"):
        currencies = redisio.hgetall("currencies")
        return currencies
    else:
        currencies = query_coins()
        redisio.hmset("currencies", currencies)
        redisio.expire("currencies", 300)
        return currencies


@app.get("/get_currencie/{coin}")
def get_currencies_coin(coin: str):
    if coin not in ['USD', 'EUR', 'CNY', 'ILS']:
        return {'message': 'Coin not in our listing'}
    if redisio.exists("currencies"):
        currencies = redisio.hgetall("currencies")
        currencies = {key.decode(): float(value.decode()) for key, value in currencies.items()}
        return {f'{coin}': currencies[coin]}
    else:
        currencies = query_coins()
        redisio.hmset("currencies", currencies)
        redisio.expire("currencies", 300)
        return {f'{coin}': currencies[coin]}


@app.get("/get_total_rub/{coin}/{total}")
def get_total_rub(coin: str, total: float):
    if coin not in ['USD', 'EUR', 'CNY', 'ILS']:
        return {'message': 'Coin not in our listing'}
    if redisio.exists("currencies"):
        currencies = redisio.hgetall("currencies")
        currencies = {key.decode(): float(value.decode()) for key, value in currencies.items()}
        return {f'{total} {coin} in rub': currencies[coin] * total}
    else:
        currencies = query_coins()
        redisio.hmset("currencies", currencies)
        redisio.expire("currencies", 300)
        return {f'{total} {coin} in rub': currencies[coin] * total}


@app.get("/get_total_coin/{coin}/{total}")
def get_total_coin(coin: str, total: float):
    if coin not in ['USD', 'EUR', 'CNY', 'ILS']:
        return {'message': 'Coin not in our listing'}
    if redisio.exists("currencies"):
        currencies = redisio.hgetall("currencies")
        currencies = {key.decode(): float(value.decode()) for key, value in currencies.items()}
        return {f'{total} rub in {coin}': total / currencies[coin]}
    else:
        currencies = query_coins()
        redisio.hmset("currencies", currencies)
        redisio.expire("currencies", 300)
        return {f'{total} rub in {coin}': total / currencies[coin]}


@app.get("/status")
def status():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return {'message': f'{dt_string}: API is Alive'}
