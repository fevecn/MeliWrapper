import requests

def api():
    endpoint = 'https://api.mercadolibre.com/oauth/token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'client_id': '',
        'client_secret': '',
        'refresh_token': '',
    }

    response = requests.post(endpoint, headers=headers, data=data)
    return response.json()

start = api()
print(start)
