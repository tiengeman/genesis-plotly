
# Genesis

Sistema de gerenciamento de faturamento em python e banco de dados MongoDB.

>🚧 Work in Progress (WIP) 

<br>

## Índice

- [Instalação](#-instalação)
- [Estrutura do codigo](#-estrutura-do-codigo)

<br>

## Instalação


**Pré-requisitos**


Certifique-se de ter os seguintes pré-requisitos instalados:

 * [Python](https://www.python.org/downloads/)  
    * Dash
    * Pandas 
    * Pymongo 
    * OracleDB 

 * [Git](https://git-scm.com/download/win)

<br/>

<details>
<summary>
    Instalando bibliotecas
</summary>

**Dash**

<a href="https://dash.plotly.com/installation"><img src="https://img.shields.io/badge/Dash-2.16.1-ff69b4"></a>

```
 > pip install dash
```

**Pandas**

<a href="https://pandas.pydata.org/docs/getting_started/install.html"><img src="https://img.shields.io/badge/Pandas-2.2.2-1EAEDB"></a>

```
 > pip install pandas
```

**Pymongo**

<a href="https://www.mongodb.com/docs/drivers/pymongo/"><img src="https://img.shields.io/badge/Pymongo-4.6.3-dec0dOS"></a>

```
 > pip install pymongo
```

**OracleDB**

<a href="https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html"><img src="https://img.shields.io/badge/OracleDB-1.4.2-ff1414"></a>

```
 > pip install oracledb
```

**Openpyxl**

<a href="https://openpyxl.readthedocs.io/en/stable/tutorial.html"><img src="https://img.shields.io/badge/Openpyxl-3.1.2-ffdb58"></a>

```
 > pip install openyxl
```
</details>

**Clonando o repositório**
>Também é possível iniciar o projeto com o GitHub Codepaces, ao navegar para `<>Code`, selecionar Codespace e clicar em `Create codespace on main`.
<br/>


```
$ git clone https://github.com/tiengeman/genesis-plotly

$ cd genesis-plotly

$ python app.py
```

[![Design sem nome](https://github.com/tiengeman/genesis-plotly/assets/167530396/03a7c5c1-005c-405c-9c66-3d684a14f695)](https://github.com/tiengeman/genesis-plotly/assets/167530396/45bd2532-1b48-44f9-8681-0779e925d44a)


<br>
 
## Estrutura do codigo

### 🗀 FRONT END

#### `app.py`

O código cria um aplicativo web interativo que exibe tabelas de desempenho mensal por competência, permitindo ao usuário selecionar diferentes competências através de uma lista suspensa e visualizar os dados formatados em tabelas.

Os módulos importados são o framework Dash para interface, e as funções definidas nos arquivos `banco.py` e `back.py`.

Define um dicionário de cores para ser utilizado no estilo do aplicativo.
```
colors = {
    'background': '#F8F8F8',  # Cinza claro para o fundo da página
    'text': '#333333',        # Cor de texto principal em preto
    'orange': '#FF4E00',      # Laranja
    'white': '#FFFFFF',       # Branco
    'gray': '#CCCCCC'         # Cinza claro para elementos secundários
}
```

O código define um layout que consiste em um título, uma lista suspensa(dropdown) e uma área para exibir a tabela selecionada. A função atualiza a tabela exibida com base na seleção feita na lista suspensa.

A função `tabela(selecao)` retorna um DataFrame com os dados de desempenho mensal por competência.

```
def atualizar_tabela(selecao):
    if selecao:
        df_tabela = tabela(selecao)
        ...
```

O código define duas callbacks que atualizam as tabelas quando um item é selecionado no dropdown. As callbakcs chamam as funções atualizar_tabela e atualizar_tabela2.

```
@app.callback(
    Output('tabela-container', 'children'),
    [Input('minha-lista-suspensa', 'value')]
)
```

As funções `atualizar_tabela` e `atualizar_tabela2` são responsáveis por criar e atualizar tabelas com base na seleção feita no dropdown. Elas obtêm os dadso da tabela através de funções tabela e tabela2, aplicam formatação aos dados numéricos para o estilo brasileiro e retorna, tabelas formatadas em formato Dash DataTable.

A tabela é formatada usando a classe `dash_table.DataTable`. Cada coluna tem um nome, ID e um tipo de dado associado. Algumas colunas possuem valor monetário.

O código verifica se o script está sendo executado diretamnete e, nesse caso, inicia o servidor Dash com a opção de depuração ativada.

#### `banco.py`

Analisa e resume dados financeiros relacionados a contratos e despesas.

A função tabela cria tabela resumo com base no mês fornecido. Ela chama algumas funções para gerar listas de dados que são usadas para criar um Dataframe.


```
def tabela(mes): 
    lista_contrato, lista_soma_comp, lista_cc = back.medicao(mes)
    ...
```

A função `tabela_2(mes)` gera uma tabela diferente com base em gastos para investimento da empresa.
```
def tabela_2(mes):
    lista_contrato = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    list_local = ['CAPEX']*len(lista_contrato)
```

A função `inativo` determina se um contrato está inativo com base nos valores fornecidos.

```
def inativo(lista_valores): 
    lista_inativo = []
    ...
```

A função `ordena_lista`  recebe a lista de contratos e uma lista de tuplas(contrato,valor) e retorna uma lista de valores ordenada de acordo com a lista de contratos.

```
def ordena_lista(lista_contrato, lista_desp): 
    lista_apoio = []
    for i in lista_contrato:
        flag = False              
        ...  
```

Função `subtrair_listas` recebe duas listas e retorna uma nova lista contendo a subtração dos elementos.

```
def subtrair_listas(lista1, lista2):
    # Verifica se as listas têm o mesmo comprimento
    if len(lista1) != len(lista2):
        return "As listas precisam ter o mesmo comprimento!"
```

Função `perc` recebe duas listas e retorna uma lista contendo o percentual de cada elemento da segunda lista em relação ao correspondente na primeira lista.

```
def perc(lista_soma_comp, list_lucro): 
    lista_perc = []
    for i in range(len(lista_soma_comp)):
    ...
```

Função `merge_list_into_tuples` recebe duas listas e as combina em uma lista de tuplas.
Um dataframe do pandas é criado usando os dados gerados pelas funções anteriores.

`medicao_capex(mes)` calcula as medições para os contratos de capital dos meses.
```
def medicao_capex(mes):
    lista_capex = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    medicao = []
```

`medicao_capex_total` calcula as medições totais para os contratos de capital.
```
def medicao_capex_total():
    lista_capex = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', 'DEPÓSITOS JUDICIAIS', 'ENGEMAN TECNOLOGIAS']
    medicao_total = []
```


Função `remove_capex` remove os contratos de capital da listade cotratos, valores e centros de custo.

```
def remove_capex(lista_contratos, lista_valor, lista_cc):
    lista_capex = ['INVESTIMENTOS (CONTRATO)', 'EXPANSÃO - FILIAL MACAÉ', 'EXPANSÃO - MATRIZ RECIFE', ...]
```

O código lida com dados de contratos, medições, despesas e lucros, organizando-os em tabelas para a análise visualização.

#### `requerimentos.txt`
Mostra as bibliotecas python e as versões com recursos utilizados nos códigos.

<br>

### 🗀 BACK

#### `__init__.py`

Importa todos os arquivos da pasta back e suas funções.

#### `banco_teste.py`

* Parte dos import :  MongoClient, ServerApi.

* Conexão com o banco de dados Mongodb utilizando username, senha e endereço. Está conectando o banco Project e a coleção "Despesas relatório".


#### `despesasrel.py`

A função `insert_despesasrel` define os parâmetros de conexão com o banco de dados Mega.

```bash
Def insert_despesasrel(collection):
host = 'dbconnect.megaerp.online' 
```

Também define uma consulta utilizando muitas tabelas e junções para buscar as informações da tabela "Despesas" no banco. A consulta é executada e é criado um dicionário Python contendo as informações e adiciona esse dicionário à lista 'documents'. 

#### `queries.py`

Sistema de análise de dados financeiros e de medição de projeto, onde as informações são extraídas no banco de dados MongoDb e manipuladas para cálculos e apresentação de resultados.

A função `pega_contratos` recupera a lista de descrições de contratos da coleção "Cotratos" do MongoDB.

```
def pega_contratos(db):
    lista_desc = []
    lista_projs = []
```

Essa função calcula o valor total das despesas financeiras, folha e de relatóroi para cada contrato. Ela recebe como entrada objeto do banco de dados e uma lista de contratos e retorna uma lista de tuplas, onde cada tupla contém o nome do contrato e o valor total das despesas associadas a esse contrato.

```
def total_despesa(db,contratos):

    soma_total = 0
```
Calcula o valor total das despesas para cada contrato em uma competência específica. Ela recebe como entrada o objeto do banco de dados, uma competência, e uma lista de contratos, retornando uma lista de tuplas com oo nome do contrato e o valor total das despesas para essa competência.

```
def total_despesa_competencia(db,competencia,contratos):

    soma_total = 0
    lista_final = []
    colecao_despesa_financeiro = db.get_collection('Despesas Financeiro')
    colecao_despesa_folha = db.get_collection('Despesas Folha')
    colecao_despesa_relatorio = db.get_collection('Despesas Relatório')
```

A função `medicao` retorna uma lista de descrições de projetos centro de custp e totais de medição par uma competencia específicas.

```
def medicao(competencia, db=back.db):

    colecao_medicao = db.get_collection('Receitas')
    ...
```

A função `medicao_total` é similar a `medicao`, mas calcula para todas as competências.
```
def medicao_total(db=back.db):

    colecao_med_total = db.get_collection('Receitas')
    ...
```


A função `competencia` retorna uma lista de todas as competencias presente na coleção de "Receitas".

```
def competencias(db=back.db):
    colecao_competencia = db.get_collection('Receitas')
    filtro = colecao_competencia.distinct('competencia-medicao')
```

Ordena uma liistta de datas no formato "mês/ano" de forma cronológica.
```
def ordenar_datas(lista):
    meses = {
        'janeiro': 1,
        'fevereiro': 2,
        ...
    }
```


<br>

### 🗀 Queries_mega

#### `filiais.py` 

As importações incluem as bibliotecas oraclesb para se conectar ao banco de dados Mega, pandas para manipulação de dados e openpyxl para trabalhar com arquivos excel.

Na função `pega filiais`, primeiro define os parâmetros para a conexão com o banco. A consulta sql seleciona informações sobre as filiais. 

O resultado da consulta vai para a lista `filiais`:

``` 
    for filial in cursor.execute(consulta):
      filiais.append(filial)

    return filiais

retorno = pega_filiais()
```
---

#### `rel_notas.py`
Esse código se conecta com o banco de dados Mega, realiza uma consulta e retorna informações sobre despesas relacionadas a recebimentos de itens.

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


### Pastas e arquivos
___

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

```

| Bibliotecas Python                                   |                        |
|------------------------------------------------------|------------------------|
| ![Dash](https://img.shields.io/badge/Dash-2.16.1-ff69b4) | > pip install dash     |
| ![Pandas](https://img.shields.io/badge/Pandas-2.2.2-1EAEDB)                                               | > pip install pandas   |
| ![Pymongo](https://img.shields.io/badge/Pymongo-4.6.3-dec0dOS)                                             | > pip install pymongo  |
| ![Openpyxl](https://img.shields.io/badge/Openpyxl-3.1.2-ffdb58)                                             | > pip install openpyxl |
| ![Oracledb](https://img.shields.io/badge/OracleDB-1.4.2-ff1414)                                             | > pip install oracledb |                                         | > pip install oracledb |

