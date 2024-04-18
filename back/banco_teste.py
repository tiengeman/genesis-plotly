from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# CONEXÃO COM O BANCO MONGO
username = 'ianfelipe'
password = 'MateMatica16'
valor_despesa = 0

uri = f"mongodb+srv://{username}:{password}@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Project']


colecao = db.get_collection('Despesas Relatório')