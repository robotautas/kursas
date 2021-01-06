import requests

url = 'https://api.frankfurter.app/'

def get_currencies():
   return list(requests.get(url + 'currencies').json().keys())
  
def get_data(amount, cur1, cur2):
    try:
        r = requests.get(url + f'latest?amount={amount}&from={cur1}&to={cur2}').json()
        return f"{amount} {cur1} = {r['rates'][cur2]} {cur2}"
    except Exception as e:
        return 'ERROR! \n' + str(e)


