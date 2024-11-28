import pandas
import requests
import pandas as pd
import os

# Ajuste o número de linhas e colunas exibidas
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
# Mostra todo o conteúdo da célula
pd.set_option('display.max_colwidth', None)  # Usando None em vez de -1, que está obsoleto
# Corrigido o caminho do arquivo e a leitura das colunas
df = pd.read_excel(r"C:\Users\felip\Desktop\dataset.xlsx")

class Cadastro:

    def __init__(self, ml_api_key, base_url="https://api.mercadolibre.com/"):
        self.ml_api_key = ml_api_key
        self.base_url = base_url

    def predcat(self, titulo):
        endpoint = f"{self.base_url}sites/MLB/domain_discovery/search?q={titulo}"
        headers = {
            "Authorization": f"Bearer {self.ml_api_key}",
        }

        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            return None
        return response.json()

    def atributos(self, category_id):
        endpoint = f"{self.base_url}categories/{category_id}/attributes"
        headers = {
            "Authorization": f"Bearer {self.ml_api_key}",
        }
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def medidas(self, domain_id):
        endpoint = f"{self.base_url}domains/{domain_id}/technical_specs"
        headers = {
            "Authorization": f"Bearer {self.ml_api_key}",
        }
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def imagens(self, diretorio_base):
        endpoint = f"{self.base_url}pictures/items/upload"
        headers = {
            "Authorization": f"Bearer {self.ml_api_key}"
        }

        respostas = []
        extracted_ids = []
        filenames = os.listdir(diretorio_base)

        for i, filename in enumerate(filenames, start=1):
            filepath = os.path.join(diretorio_base, filename)
            print(f"Trying to upload {filepath}")  # Debugging line

            with open(filepath, 'rb') as f:
                files = {'file': (filename, f)}
                response = requests.post(endpoint, headers=headers, files=files)

                if response.status_code == 201:
                    response_json = response.json()
                    respostas.append(response_json)
                    extracted_ids.append(response_json.get('id'))
                else:
                    print(f'Erro: {response.status_code}')
                    print(response.text)
    
        return extracted_ids



    def cadastrar(self, titulo, preco, categoria, fotos, atributos):
        endpoint = f"{self.base_url}items"
        print(preco)
        headers = {
            "Authorization": f"Bearer {self.ml_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "title": titulo,
            "category_id": categoria,
            "price": preco,
            "currency_id": "BRL",
            "available_quantity": 10,
            "buying_mode": "buy_it_now",
            "condition": "new",
            "listing_type_id": "gold_pro",
            "sale_terms": [
                {"id": "WARRANTY_TYPE", "value_name": "Garantia do vendedor"},
                {"id": "WARRANTY_TIME", "value_name": "30 dias"}
            ],
            "pictures": [
                {
                    "source": fotos
                }
            ],
            "attributes": atributos
        }
        try:
            response = requests.post(endpoint, headers=headers, json=data)
        except BaseException as err:
            print(f'{err = }\n\n{data = }\n\n\n\n')
            return None

        return response.json()


cadastro = Cadastro(ml_api_key="APP_USR-7500806246647047-111010-175e44348a057cf8d8e85b66458aee15-276188176")

df_filtered = df.dropna(subset=['Titulo'])


# Descobre a categoria do produto com base no título (pode falhar)
categories = list(df_filtered['Titulo'].apply(cadastro.predcat))


# Transforma as categorias do dataframe em matriz
matriz = []
for lista in categories:
    matriz.append(lista[0])


# Pega o category_id e o category_name
category_info = [{"category_id": entry["category_id"], "category_name": entry["category_name"]} for entry in matriz]


category_id = [entry["category_id"] for entry in category_info]
category_name = [entry["category_name"] for entry in category_info]

# Coloca o nome da categoria junto com o título de cada produto
df_filtered['Categoria'] = category_name

# Cria um dataframe para cada categoria e coloca os respectivos produtos lá
dict_dataframes = {nome: pd.DataFrame(None) for nome in category_name}

# Itera as chaves do dicionário como se fosse uma lista
for nome_df in dict_dataframes.keys():
    # Filtrar df_filtered para as linhas onde a 'Categoria' corresponde ao nome do DataFrame
    dict_dataframes[nome_df] = df_filtered[df_filtered['Categoria'] == nome_df].copy()


# Pega os atributos para a categoria prevista
atributos_list = [cadastro.atributos(i) for i in category_id]

# Separa em atributos requeridos, opcionais e totais
atributos_req = [[item.get('name', None) for item in sublist if item.get('tags', {}).get('required', False)] for sublist in atributos_list]
atributos_opt = [[item.get('name', None) for item in sublist if not item.get('tags', {}).get('required', False)] for sublist in atributos_list]
atributos_all = [req + opt for req, opt in zip(atributos_req, atributos_opt)]
print(atributos_req)

exit()
# Novas colunas para o Dataframe com os atributos obrigatórios para a categoria
novas_colunas = ['Preço', 'Quantidade']

for nome_df in dict_dataframes.keys():
    # Adiciona as colunas e atributos requeridos para cada dataframe (em que cada um representa uma categoria)
    dict_dataframes[nome_df] = [df[atributos_req] for elementos in atributos_req]

# Agora salvando no Excel
nome_arquivo_excel = 'dataset2.xlsx'
with pd.ExcelWriter(nome_arquivo_excel) as writer:
    for nome_df, df in dict_dataframes.items():
        # Verifique se o dataframe não está vazio antes de salvar
        if not df.empty:
            df.to_excel(writer, sheet_name=nome_df)


# Configurações Globais de atributos
global_config = {'Marca': 'Hypnose', 'Quantidade de peças': '1', "Temporada de lançamento": '2023'}
tamanho_infantil = [1, 2, 3, 4, 6, 8, 10, 12, 14, 16]
tamanho_adulto = ['PP', 'P', 'M', 'G', 'GG']

# Captura o primeiro valor de cada coluna
first_row_values = df.iloc[0]

# Cria uma lista de dicionários com 'name' e 'value_name' para cada coluna
atributos_publi = [{'name': col_name, 'value_name': first_row_values[col_name]} for col_name in df.columns]

print(atributos_publi)

# Tabela de medidas


# Imagens

#   Lista de caminhos de arquivos que você deseja enviar
# Diretório base onde os arquivos estão localizados
diretorio_base = 'D:\\Users\\felip\\Pictures\\Hypnose\\Halloween\\JPEG'

pic_id = cadastro.imagens(diretorio_base)

novas_colunas = ['pic_id']

print(pic_id)

df['pic_id'] = None
df.at[0, 'pic_id'] = pic_id

# Mandar pro Excel
df.to_excel(r'C:\Users\felip\Desktop\dataset2.xlsx', index=False)
# Publicação
print(df)

#publicar = cadastro.cadastrar(titulo = df_filtered , preco= df['Preço'], categoria= , fotos= , atributos= )
exit()
# Ignora daqui pra baixo ////////////////////////////////////

df2 = pd.DataFrame.from_dict({f'Category_{i+1}': col for i, col in enumerate(atributos_all)},orient='index').transpose()

# To find the intersection of all columns, we convert each column to a set and then find the intersection of those sets.
# We use dropna() to exclude any NaN values from each column.
common_elements_intersection = set(df2.iloc[:, 0].dropna())
for col in df2.columns[1:]:
    common_elements_intersection &= set(df2[col].dropna())

# Update atributos_all to only include elements that are common across all DataFrame columns
atributos_all = list(common_elements_intersection)

# Add a new column to df2 containing the common intersection elements (atributos_all)
# First, ensure df2 is long enough to hold all the common elements
if len(df2) < len(atributos_all):
    for _ in range(len(atributos_all) - len(df2)):
        df2.loc[len(df2)] = None

# Populate the new column with common intersection elements
df2['Intersection_Of_All_Columns'] = atributos_all + [None] * (len(df2) - len(atributos_all))


# df2.to_excel(r'C:\Users\felip\Desktop\dataset3.xlsx', index=False)
