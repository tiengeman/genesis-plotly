import pandas as pd
import banco_teste
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


def total_despesa(db):

    soma_total = 0
    colecao_despesa_financeiro = db.get_collection('Despesas Financeiro')
    colecao_despesa_folha = db.get_collection('Despesas Folha')
    colecao_despesa_relatorio = db.get_collection('Despesas Relatório')

    pipeline_financeiro =  [ 
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_financeiro':{'$sum':'$valor-original-despesa'}}}
    ]
    pipeline_folha  = [
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_folha':{'$sum':'$valor-original-despesa'}}}
    ]
    pipeline_relatorio = [
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_relatorio':{'$sum':'$valor-original-despesa'}}}
    ]

    total_financeiro = colecao_despesa_financeiro.aggregate(pipeline_financeiro)
    total_folha = colecao_despesa_folha.aggregate(pipeline_folha)
    total_relatorio = colecao_despesa_relatorio.aggregate(pipeline_relatorio)

    dicio_financeiro = {}
    dicio_folha = {}
    dicio_relatorio = {}

    lista_final = []

    for i in total_financeiro:
        dicio_financeiro[i['_id']['descricao-projeto']] = i['despesa_financeiro']

    for j in total_folha:
        dicio_folha[j['_id']['descricao-projeto']] = j['despesa_folha']
    
    for k in total_relatorio:
        dicio_relatorio[k['_id']['descricao-projeto']] = k['despesa_relatorio']

    for total in dicio_relatorio:
        soma_total += dicio_financeiro[total]
        soma_total += dicio_folha[total]
        soma_total += dicio_relatorio[total]
        lista_final.append((total,soma_total))
    
    return lista_final


def medicao(db,competencia):

    colecao_medicao = db.get_collection('Receitas')

    # consulta que agrupa as receitas por descrição do projeto e soma o campo de valor de medição
    pipeline = [
        {"$match": {"competencia-medicao": competencia}},  # Filtrar por data
        {"$group": {"_id": {"descricao-projeto": "$descricao-projeto",'codigo-projeto-unificado':'$codigo-projeto-unificado'}, "total-medicao": {"$sum": "$valor-medicao"}}}  # Calcular a soma da receita
    ]

    medicao = colecao_medicao.aggregate(pipeline)

    lista_descricao_projeto = []
    lista_centro_de_custo = []
    lista_total_medicao = []

    for i in medicao:
        lista_descricao_projeto.append(i["_id"]["descricao-projeto"])
        lista_centro_de_custo.append(i['_id']['codigo-projeto-unificado'])
        lista_total_medicao.append(i["total-medicao"])
        

    return lista_descricao_projeto,lista_total_medicao,lista_centro_de_custo

def medicao_total(db):

    colecao_med_total = db.get_collection('Receitas')

    pipeline = [
        {"$group": {"_id": {"descricao-projeto": "$descricao-projeto",'codigo-projeto-unificado':'$codigo-projeto-unificado'}, "total-medicao": {"$sum": "$valor-medicao"}}}  # Calcular a soma da receita
    ]

    medicao = colecao_med_total.aggregate(pipeline)


    lista_descricao_projeto = []
    lista_centro_de_custo = []
    lista_total_medicao = []

    for i in medicao:
        lista_descricao_projeto.append(i["_id"]["descricao-projeto"])
        lista_centro_de_custo.append(i['_id']['codigo-projeto-unificado'])
        lista_total_medicao.append(i["total-medicao"])

    return lista_descricao_projeto,lista_total_medicao,lista_centro_de_custo 

# função para retornar uma lista com todas as medições(pelos menos todas as presentes na aba de cad-receitas)
def competencias(db):
    colecao_competencia = db.get_collection('Receitas')

    filtro = colecao_competencia.distinct('competencia-medicao')

    return list(filtro)

a= competencias(banco_teste.db)

print(a)