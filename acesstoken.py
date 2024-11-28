import requests

def api():
    endpoint = 'https://api.mercadolibre.com/oauth/token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': '',
        'client_secret': '',
        'code': '',
        'redirect_uri': 'http://localhost:3000'
    }

    response = requests.post(endpoint, headers=headers, data=data)
    return response.json()

start = api()
print(start)
