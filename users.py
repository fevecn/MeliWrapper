import requests

class User:
    def __init__(self, ml_api_key, base_url="https://api.mercadolibre.com/"):
        self.ml_api_key = ml_api_key
        self.base_url = base_url

    def create_user(self, site_id="MLB"):
        endpoint = f"{self.base_url}users/test_user"
        headers = {
            "Authorization": f"Bearer {self.ml_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "site_id": site_id
        }

        response = requests.post(endpoint, headers=headers, json=data)
        return response.json()

mlwrapper = User(ml_api_key="")
user_data = mlwrapper.create_user(site_id="MLB")
print(user_data)