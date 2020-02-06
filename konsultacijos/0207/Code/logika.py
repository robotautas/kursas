import requests
import json

def get_10_ids(num):
    response = requests.get('https://api.coinlore.com/api/tickers/').json()
    response_cleaned = []
    for i in response['data'][:int(num)+1]:
        if i['symbol'] != 'USDT':
            response_cleaned.append({'coin': i['name'], 'symbol': i['symbol'], 'id': i['id']})
    return response_cleaned


def get_best_rates(id, symbol):
    shitty_exchanges = ['BCex', 'CHAOEX', 'ZB.com']
    response = requests.get(f'https://api.coinlore.com/api/coin/markets/?id={id}').json()
    response_cleaned = []
    for i in response:
        if i['base'] == symbol and i['name'] not in shitty_exchanges:
            response_cleaned.append({'Exchange': i['name'],'Price USD': i['price_usd']})
    sorted_list = sorted(response_cleaned, key=lambda k: k['Price USD']) 
    res = [sorted_list[0]] + [sorted_list[-1]]
    return res


def get_table(num=10):
    result = []
    for i in get_10_ids(num):
        data = get_best_rates(i['id'], i['symbol'])
        profit = (data[1]['Price USD']-data[0]['Price USD']) / data[0]['Price USD'] * 100
        result.append({
            'name': i['coin'], 
            'ex1': data[0]['Exchange'], 
            'rate1': round(data[0]['Price USD'], 4),
            'ex2': data[1]['Exchange'], 
            'rate2': round(data[1]['Price USD'], 4),
            'profit': round(profit, 2)})
    return sorted(result, key=lambda k: k['profit'])[::-1] 


