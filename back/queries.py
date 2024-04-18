import pandas as pd
# from banco import client, DB_NAME,COLLECTION_NAME


# Pega o nome dos contratos
def pega_contratos(db):
    lista_desc = []
    lista_projs = []

    collection = db.get_collection('Contratos')

    # contratos = collection['descricao-contratos']
    
    # O .distinct serve para que ele "exlua" as duplicatas dos nomes dos contratos na hora da consulta
    desc = collection.distinct('descricao-contratos')
    # projetos = collection.distinct('projetosapiens-contratos')


    # for d in desc:
    #     lista_desc.append(d)

    # for p in projetos:
    #     lista_projs.append(p)

    # for contrato in desc:
    #     lista_desc.append(contrato)

    # desc é uma lista com os nomes dos contratos
    return desc


def total_despesa(colle,competencia,list_desc_projeto):
    valor_despesa = 0
    lista_despesas = []
    
    # Loop externo que pega a lista de projetos
    for desc_projeto in list_desc_projeto:
        response = colle.find({'competencia-despesa':competencia, 'descricao-projeto': desc_projeto})
        # Loop interno que calcula o total de despesas para cada projeto da lista
        for a in response:
            despesa = a['valor-original-despesa']
            despesa = despesa.replace(',', '')
            valor_despesa += float(despesa)
        
        lista_despesas.append(valor_despesa)
        valor_despesa = 0
        # lista_dicios  = list(response)

    # frame = pd.DataFrame(lista_dicios)
    # frame = frame.drop('_id',axis=1)


    # for documento in lista_dicios:
    #     for chave, valor in documento.items():
    #         if isinstance(valor, str):
    #             try:
    #                 valor.encode('utf-8')
    #                 print('Deu certo')
    #             except UnicodeEncodeError:
    #                 print(f'Chave: {chave}, Valor: {valor}')

    # frame.to_excel('teste_retorno_mongo.xlsx')
    return lista_despesas


def medicao(db, competencia):

    colecao_medicao = db.get_collection('Receitas')

    # consulta que agrupa as receitas por descrição do projeto e soma o campo de valor de medição
    pipeline = [
        {"$match": {"competencia-medicao": competencia}},  # Filtrar por data
        {"$group": {"_id": {"descricao-projeto": "$descricao-projeto"}, "total-medicao": {"$sum": "$valor-medicao"}}}  # Calcular a soma da receita
    ]

    medicao = colecao_medicao.aggregate(pipeline)
    lista_descricao_projeto = []
    lista_total_medicao = []

    for i in medicao:
        lista_descricao_projeto.append(i["_id"]["descricao-projeto"])
        lista_total_medicao.append(i["total-medicao"])

    return lista_descricao_projeto, lista_total_medicao