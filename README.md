# Genesis

Sistema de gerenciamento de faturamento em python e banco de dados MongoDB.

>🚧 Work in Progress (WIP) 

<br>

## Indice

- [Instalação](#-instalação)
- [Estrutura do codigo](#-estrutura-do-codigo)

<br>

### Instalação
---
#### Pré-requisitos
Certifique-se de ter Python e Git pré-requisitos instalados:

 * Python  
    * Shiny 
    * Pandas 
    * Pymongo 
    * OracleDB 

 * Git

#### Execução
>Também é possível iniciar o projeto com o GitHub Codepaces, ao navegar para `<>Code`, selecionar Codespace e clicar em `Create codespace on main`.

```
# Clonando o repositório
$ git clone https://github.com/tiengeman/genesis-plotly

$ cd genesis-plotly
```

> Run teste

<h1>
  <img src="https://ik.imagekit.io/palitos/genesisrun.gif?updatedAt=1714138806739">
</h1>



<br>
 
### Estrutura do codigo
---

### 🗀 FRONT END

#### `app.py`

O código exibe dados de desempenho mensal por competência em uma tabela interativa.

Os módulos importados são o framework Dash para inetrface, e as funções definidas nos arquivos `banco.py` e `back.py`.

O código define um layout que consiste em um título, uma lista suspensa(dropdown) e uma área para exibir a tabela selecionada. A função atualiza a tabela exibida com base na seleção feita na lista suspensa.

A função tabela(selecao) retorna um DataFrame com os dados de desempenho mensal por competência.

```
def atualizar_tabela(selecao):
    if selecao:
        df_tabela = tabela(selecao)
        ...
```
A tabela é formatada usando a classe `dash_table.DataTable`. Cada coluna tem um nome, ID e um tipo de dado associado. Algumas colunas possuem valor monetário.

<br>

### 🗀 BACK

#### `__init__.py`

Importa todos os arquivos da pasta back e suas funções 

#### `banco_teste.py`

* Parte dos import :  MongoClient, ServerApi.

* Conexão com o banco mongodb utilizando username, senha e endereço. Está conectando o banco Project e a coleção "Despesas relatório" que serão exibidos em forma de tabela no arquivo `main.py`.


#### `despesasrel.py`

```bash
Def insert_despesasrel(collection):
host = 'dbconnect.megaerp.online' 
```

Essa função define os parâmetros de conexão com o banco de dados mega. 

Também define uma consulta utilizando muitas tabelas e junções para buscar as informações da tabela despesas no banco. A consulta é executada e é criado um dicionário Python contendo as informações e adiciona esse dicionário à lista 'documents'. 

#### `inserts.py`
Insere informações sobre filiais no MongoBD, sem que haja duplicação de uma filial que já existe.O código:

Pega uma função que recupera as informações sobre filiais. 
```
from queries_mega import pega_filiais
```
Obtém a coleção filiais do banco de dados usando db.get_collection('Filiais'). 
```
def inserir_filiais():
  colecao_insert = db.get_collection('Filiais')
```
E verifica se a filial já existe no banco de dados. 

```
  for filial in filiais:
    if colecao_insert.count_documents({'nome-filial':filial[0]}) == 0:
```

Se o documento não existe(retorno 0), insere a filial no banco de dados MongoDB. Os campos inseridos são: codigo-filial, nome-filial, pais-filial, estado-filial, codigo-municipio-filial, municipio-filial, cnpj-filial, inscricao-estadual. 

#### `keys.json`

Autenticação e autorização em serviços GCP. O código configura um serviço que precisa interagir com APIs do Google Cloud.

#### `queries.py`

Retorna a lista de nomes de contratos presentes na coleção 'Contratos' do banco de dados MongoDB.

```
def pega_contratos(db):
    lista_desc = []
    lista_projs = []
```
Essa função calcula o valor total das despesas para cada contrato. Ela recebe como entrada oobjeto do banco de dados e uma lista de contratos e retorna uma lista de tuplas, onde cada tupla contém o nome do contratoe o valor total das despesas associadas a esse contrato.

```
def total_despesa(db,contratos):

    soma_total = 0
```
Calcula o valor total das despesas para cada contrato em uma competência específica.Ela recebe como entrada o objeto do banco de dados, uma competência, e uma lista de contratos, retornando uma lista de tuplas com oo nome do contrato e o valor total das despesas para essa competência.

```
def total_despesa_competencia(db,competencia,contratos):

    soma_total = 0
    lista_final = []
    colecao_despesa_financeiro = db.get_collection('Despesas Financeiro')
    colecao_despesa_folha = db.get_collection('Despesas Folha')
    colecao_despesa_relatorio = db.get_collection('Despesas Relatório')
```

Consulta o valor total das medições para cada contrato em uma competência específica. Recebecomo entrada a copet~encia, uma lista de contratos e o objeto do banco de dados.


<br>

### 🗀 Queries_mega

#### `filiais.py` 

As importações incluem as bibliotecas oraclesb para se conectar ao banco de dados Mega, pandas para manipulação de dados e openpyxl para trabalhar com arquivos excel.

Na função `pega filiais`, primeiro define os parametros para a conexão com o banco. A consulta sql seleciona informações sobre as filiais. 

O resultado da consulta vai para a lista `filiais`:

``` 
    for filial in cursor.execute(consulta):
      filiais.append(filial)

    return filiais

retorno = pega_filiais()
```
---

#### `rel_notas.py`
Esse códigose conecta com o banco de dados Mega, realiza uma consulta e retorna informações sobre despesas relacionadas a recebimentos de itens.

A função `pega_infps_para_despesasrel` define variáveis de conexão com o banco de dados:

```
def pega_infps_para_despesasrel():
  host = 'dbconnect.megaerp.online'
  ...
```

A consulta envolve as tabelas EST_RECEBIMENTO, EST_ITENSRECEB, EST_ITENSRECEB_CCF, EST_ITENSRECEB_PROJ, EST_PRODUTOS, GLO_AGENTES, GLO_ACAO e Est_Desccomplemento.

```consulta = """
    SELECT 
        A.ACAO_IN_CODIGO "AÇÃO"
        ,ACAO.ACAO_ST_NOME "NOME DA AÇÃO"
        ...

      FROM mega.EST_RECEBIMENTO@engeman A   
      ...

      INNER JOIN mega.EST_ITENSRECEB@engeman B ON A.RCB_ST_NOTA       = B.RCB_ST_NOTA 
      ...

      INNER JOIN mega.EST_ITENSRECEB_CCF@engeman C ON B.RCB_ST_NOTA       = C.RCB_ST_NOTA
      ...

      INNER JOIN mega.EST_ITENSRECEB_PROJ@engeman D ON C.RCB_ST_NOTA       = D.RCB_ST_NOTA
      ...

      INNER JOIN mega.EST_PRODUTOS PROD@engeman ON B.PRO_IN_CODIGO     =  PROD.PRO_IN_CODIGO
      ...

      INNER JOIN mega.GLO_AGENTES@engeman F ON A.AGN_IN_CODIGO     = F.AGN_IN_CODIGO 
      ...

      INNER JOIN mega.GLO_ACAO@engeman ACAO ON ACAO.ACAO_IN_CODIGO = A.ACAO_IN_CODIGO
      ...

      LEFT JOIN mega.Est_Desccomplemento@engeman COMP ON COMP.RCB_ST_NOTA = B.RCB_ST_NOTA
      ...
```

A consulta retorna informações sobre ação, nome da ação, tipo de nota, número e nome do projeto,centro de custo, número da nota fiscal, código e nome do agente, item, descrição do item, valor do item por projeto, código e nome da classe financeira, e data de entrada da nota.


```shell
genesis/
├── back
│   ├── banco_teste.py
│   ├── despesasrel.py
│   ├── inserts.py
│   ├── queries.py
│   └── teste.py
├── queries_mega
│   ├── __init__.py
│   ├── filial.py
│   └── rel_notas.py
├── .gitignore
├── README
├── app.py
├── keys.json
└── banco.py
