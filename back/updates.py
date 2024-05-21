import back.banco_teste

def atualiza_projetos(lista,db=back.db):

    desc_projeto = lista[4]
    colecao = db.get_collection('Cadastro Contratos')

    colecao.update_one(
        {'descricao-contrato':desc_projeto},
        {'$set':{
            'os-contratos'              :lista[0],
            'tipo-contratos'            :lista[1],
            'enquadramento-contratos'   :lista[2],
            'cliente-contratos'         :lista[3],
            'descricao-contratos'       :lista[4],
            'icj-contratos'             :lista[5],
            'sap-contratos'             :lista[6],
            'inicio-contratos'          :lista[7],
            'fim-contratos'             :lista[8],
            'aditivos-contratos'        :lista[9],
            'valor-contratos'           :lista[1],
            'prazomes-contratos'        :lista[11],
            'prazodias-contratos'       :lista[12],
            'status-contratos'          :lista[13],
            'responsavel-contratos'     :lista[14],
            'filial-contratos'          :lista[15],
            'projeto-contratos'         :lista[16],
            'projetosapiens-contratos'  :lista[17],
            'iss-contrato'              :lista[18],
            'admcentral-contrato'       :lista[19],
            'pis-contrato'              :lista[20],
            'cofins-contrato'           :lista[21],
            'csll-contrato'             :lista[22],
            'irpj-contrato'             :lista[23],
            'icms-contrato'             :lista[24],
            'investimento-contrato'     :lista[25]
        }}
    )
