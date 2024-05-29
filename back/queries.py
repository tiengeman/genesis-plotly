import pandas as pd
import back.banco_teste
from datetime import datetime
# from banco import client, DB_NAME,COLLECTION_NAME


# Pega o nome dos contratos
def pega_contratos(db=back.db):
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


def total_despesa(db=back.db):

    soma_total = 0
    colecao_despesa_financeiro = db.get_collection('Despesas Financeiro')
    colecao_despesa_folha = db.get_collection('Despesas Folha')
    colecao_despesa_relatorio = db.get_collection('Despesas Relatório')

    # filtros que agrupam os campos descricao-projeto e somam os valores de valor-original-despesa de cada contrato
    pipeline_financeiro =  [ 
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_financeiro':{'$sum':'$valor-original-despesa'}}}
    ]
    pipeline_folha  = [
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_folha':{'$sum':'$valor-original-despesa'}}}
    ]
    pipeline_relatorio = [
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_relatorio':{'$sum':'$valor-original-despesa'}}}
    ]

    # Consultas que utilizam os filtros a cima. O retorno dessas consultas são dicionarios. Ex:. {'_id': {'descricao-projeto': 'ADM LOCAL (MACAÉ)'}, 'despesa_financeiro': 450681.34}
    total_financeiro = colecao_despesa_financeiro.aggregate(pipeline_financeiro)
    total_folha = colecao_despesa_folha.aggregate(pipeline_folha)
    total_relatorio = colecao_despesa_relatorio.aggregate(pipeline_relatorio)

    dicio_financeiro = {}
    dicio_folha = {}
    dicio_relatorio = {}

    lista_final = []
    
    # Loops para adicionar nos respectivos dicionários os valores totais dos contratos(são as chaves dos dicios) e a despesa total(que são os valores dos dicios)
    for i in total_financeiro:
        dicio_financeiro[i['_id']['descricao-projeto']] = i['despesa_financeiro']

    for j in total_folha:
        dicio_folha[j['_id']['descricao-projeto']] = j['despesa_folha']
    
    for k in total_relatorio:
        dicio_relatorio[k['_id']['descricao-projeto']] = k['despesa_relatorio']

    for contrato in dicio_relatorio:
        # aqui o código ira tentar somar o valor da despesa caso a chave contrato exista no dicionario
        try:
            soma_total += dicio_financeiro[contrato]
        except:
            pass
        try:
            soma_total += dicio_folha[contrato]
        except:
            pass
        try:            
            soma_total += dicio_relatorio[contrato]
        except:
            pass
        lista_final.append((contrato,soma_total))
        soma_total = 0
    
    return lista_final

def total_despesa_competencia(competencia, db=back.db):

    soma_total = 0
    colecao_despesa_financeiro = db.get_collection('Despesas Financeiro')
    colecao_despesa_folha = db.get_collection('Despesas Folha')
    colecao_despesa_relatorio = db.get_collection('Despesas Relatório')

    # filtros que agrupam os campos especificados e somam os valores de despesas de cada contrato
    pipeline_financeiro =  [ 
        {"$match": {"competencia-despesa": competencia}},
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_financeiro':{'$sum':'$valor-original-despesa'}}}
    ]
    pipeline_folha  = [
        {"$match": {"competencia-despesa": competencia}},
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_folha':{'$sum':'$valor-original-despesa'}}}
    ]
    pipeline_relatorio = [
        {"$match": {"competencia-despesa": competencia}},
        {'$group':{'_id':{'descricao-projeto':'$descricao-projeto'},'despesa_relatorio':{'$sum':'$valor-original-despesa'}}}
    ]

    # Consultas que utilizam os filtros a cima. O retorno dessas consultas são dicionarios. Ex:. {'_id': {'descricao-projeto': 'ADM LOCAL (MACAÉ)'}, 'despesa_financeiro': 450681.34}
    total_financeiro = colecao_despesa_financeiro.aggregate(pipeline_financeiro)
    total_folha = colecao_despesa_folha.aggregate(pipeline_folha)
    total_relatorio = colecao_despesa_relatorio.aggregate(pipeline_relatorio)

    dicio_financeiro = {}
    dicio_folha = {}
    dicio_relatorio = {}

    lista_final = []

    # Loops para adicionar nos respectivos dicionários os valores totais dos contratos(são as chaves dos dicios) e a despesa total(que são os valores dos dicios)
    for i in total_financeiro:
        dicio_financeiro[i['_id']['descricao-projeto']] = i['despesa_financeiro']

    for j in total_folha:
        dicio_folha[j['_id']['descricao-projeto']] = j['despesa_folha']
    
    for k in total_relatorio:
        dicio_relatorio[k['_id']['descricao-projeto']] = k['despesa_relatorio']

    for contrato in dicio_relatorio:
        try:
            soma_total += dicio_financeiro[contrato]
        except:
            pass
        try:
            soma_total += dicio_folha[contrato]
        except:
            pass
        try:            
            soma_total += dicio_relatorio[contrato]
        except:
            pass
        
        lista_final.append((contrato,soma_total))
        soma_total = 0
    
    return lista_final


def medicao(competencia, db=back.db):

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

def medicao_total(db=back.db):

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
def competencias(db=back.db):
    colecao_competencia = db.get_collection('Receitas')

    filtro = colecao_competencia.distinct('competencia-medicao')
    comp = ordenar_datas(list(filtro))

    return comp

# Função que irá retornar uma lista de listas de alguns dos elementos da tabela de Cadastro Impostos
def cad_impostos(db=back.db):
    colecao_impostos = db.get_collection('Cadastro Impostos')

    # Filtro que puxa apenas as colunas especificadas
    filtro = colecao_impostos.find({},{'receitatotal-impostos':1,'pisretido-impostos': 1,'pispago-impostos': 1,'cofinsretido-impostos': 1,'cofinspago-impostos': 1,'datafechamento-impostos':1,'competencia-impostos':1})
    lista = []

    for i in filtro:
        valores = i.values()
        lista.append(list(valores))
        
    return lista

# Função que irá retornar uma lista de listas de todos os elementos da tabela de Cadastro Encargos
def cad_encargos(db=back.db):
    colecao = db.get_collection('Cadastro Encargos')
    lista = []
    lista_cc = []

    for i in colecao.find():
        valores = list(i.values())
        lista.append(valores)
        lista.append(valores[2])

    return lista,lista_cc

# Função que irá retornar uma lista de listas de todos os elementos da tabela de Cadastro Contratos
def cad_contratos(db=back.db):
    colecao = db.get_collection('Cadastro Contratos')

# lista que vai guardar todos elementos que tem na tabela Cadastro Contratos
    lista = []
    for i in colecao.find():
        valores = i.values()
        lista.append(list(valores))

    return lista

def ordenar_datas(lista):
    # Define um dicionário para mapear os meses para seus números correspondentes
    meses = {
        'janeiro': 1,
        'fevereiro': 2,
        'março': 3,
        'abril': 4,
        'maio': 5,
        'junho': 6,
        'julho': 7,
        'agosto': 8,
        'setembro': 9,
        'outubro': 10,
        'novembro': 11,
        'dezembro': 12
    }
    # Converte cada elemento da lista para um formato que possa ser ordenado facilmente
    lista_formatada = [(int(ano), meses[mes], 1) for mes, ano in [data.split('/') for data in lista]]
    # Ordena as datas formatadas
    lista_ordenada = sorted(lista_formatada)
    # Converte as datas ordenadas de volta para o formato original
    lista_ordenada = [f"{datetime(ano, mes, dia).strftime('%B').lower()}/{ano}" for ano, mes, dia in lista_ordenada]
    # Substitui os nomes dos meses de inglês para português
    meses_pt = {
        'january': 'janeiro',
        'february': 'fevereiro',
        'march': 'março',
        'april': 'abril',
        'may': 'maio',
        'june': 'junho',
        'july': 'julho',
        'august': 'agosto',
        'september': 'setembro',
        'october': 'outubro',
        'november': 'novembro',
        'december': 'dezembro'
    }
    lista_ordenada = [data.replace(datetime.strptime(data.split('/')[0], '%B').strftime('%B').lower(), meses_pt[datetime.strptime(data.split('/')[0], '%B').strftime('%B').lower()]) for data in lista_ordenada]

    return lista_ordenada
