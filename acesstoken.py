#http://localhost:3000/?code=TG-65023344ba6caa00010bf733-276188176&state=
#APP_USR-7500806246647047-091318-ba30742b80087d70df496477e02160d9-276188176
import requests

def api():
    endpoint = 'https://api.mercadolibre.com/oauth/token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': '7500806246647047',
        'client_secret': 'Ww0c5SdsmCU9ns6Ca0WWl9GKtN2u4A6P',
        'code': 'TG-65023a72c0fb010001ee4f69-276188176',
        'redirect_uri': 'http://localhost:3000'
    }

    response = requests.post(endpoint, headers=headers, data=data)
    return response.json()

start = api()
print(start)
