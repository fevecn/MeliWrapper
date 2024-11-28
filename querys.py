import requests
import json

class Melipper:
    def __init__(self, base_url="https://api.mercadolibre.com/"):
        self.base_url = base_url

    def token(self):
        endpoint = f'{self.base_url}oauth/token'
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
        data = response.json()
        access_token = data['access_token']
        self.ml_api_key = access_token
        refresh_token = data['refresh_token']
        return [refresh_token, access_token]

    def search_product_by_gtin(self, gtin):
        endpoint = f'{self.base_url}products/search?status=active&site_id=MLB&product_identifier={gtin}'
        headers = {"Authorization": f"Bearer {self.ml_api_key}"}
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_item_id(self, product_id):
        endpoint = f"{self.base_url}products/{product_id}"
        headers = {"Authorization": f"Bearer {self.ml_api_key}"}
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_category_and_catalog_id(self, item_id):
        endpoint = f"{self.base_url}items/{item_id}"
        headers = {"Authorization": f"Bearer {self.ml_api_key}"}
        response = requests.get(endpoint, headers=headers)
        json_data = response.json()
        return json_data

    def publicar(self, gtin):
        product = melipper.search_product_by_gtin(gtin)
        product_id = product.get('results', [{}])[0].get('id', None)

# Buscar item_id usando product_id
        if product_id:
            item = melipper.get_item_id(product_id)
            item_id = item.get('buy_box_winner', {}).get('item_id', None)

# Buscar category_id e catalog_product_id usando item_id
        if item_id:
            final_ids = melipper.get_category_and_catalog_id(item_id)
            category_id = final_ids.get('category_id')
            catalog_product_id = final_ids.get('catalog_product_id')

        endpoint = f"{self.base_url}items"
        headers = {"Authorization": f"Bearer {self.ml_api_key}", "Content-Type": "application/json"}
        data = {
            "site_id": "MLB",
            "category_id": category_id,
            "price": 300,
            "condition": "new",
            "currency_id": "BRL",
            "available_quantity": 1,
            "buying_mode": "buy_it_now",
            "listing_type_id": "gold_pro",
            "catalog_product_id": catalog_product_id,
            "catalog_listing": True
        }
        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        return response.json()

#Cria um nickname para a Classe
melipper = Melipper()

#Renova Token
print(melipper.token())

#Procura um produto usando o GTIN como base
#print(melipper.search_product_by_gtin(7896839928010))

#Pega o id de item usando o código do produto como base
#print(melipper.get_item_id(product_id))

#Pega o id de categoria e catalogo usando o id de item
#print(melipper.get_category_and_catalog_id(item_id))

#Publica um item como catalogo do ML usando o código GTIN
#print(melipper.publicar(gtin)

