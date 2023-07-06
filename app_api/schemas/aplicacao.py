from pydantic import BaseModel
from typing import Optional, List
from model.aplicacao import Aplicacao


class AplicacaoSchema(BaseModel):
    """ Define uma nova aplicação a ser inserida ou atualizada deve ser representada (aplicacao.py)
    """
    id:         int = 0
    nome:       str = "SAP Success Factor"
    sigla:      str = "SSF"
    descricao:  str = "O SAP SuccessFactors é uma solução completa para um RH estratégico e eficaz."
    status:     str = "AA"


class AplicacaoViewSchema(BaseModel):
    """ Define como uma aplicação será retornada (aplicacao.py)
    """
    id:         int = 1
    nome:       str = "SAP Success Factor"
    sigla:      str = "SSF"
    descricao:  str = "SAP Success Factor"
    status:     str = "AA"

class ListagemAplicacoesSchema(BaseModel):
    """ Define como uma listagem de aplicações será retornada (aplicacao.py)
    """
    aplicacoes:List[AplicacaoSchema]

# As funções da classe do schemas não podem conter espaços iniciais (identação)
# Pois ocorre erro de importação/utilização no app.py
def apresenta_aplicacoes(aplicacoes: List[Aplicacao]):
    """ Retorna uma representação da aplicação seguindo o schema definido em
        AplicaçãoViewSchema. (aplicacao.py)
    """
    result = []
    for aplicacao in aplicacoes:
        result.append({
            "id"        : aplicacao.id,
            "nome"      : aplicacao.nome,
            "sigla"     : aplicacao.sigla,
            "descricao" : aplicacao.descricao,
            "status"    : aplicacao.status
        })
        
    return {"aplicacoes": result}

class AplicacaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura de dado retornado após uma requisição de remoção (aplicacao.py)
    """
    mesage: str
    nome:   str

def apresenta_aplicacao(aplicacao: Aplicacao):
    """ Retorna uma representação da aplicacao seguindo o schema definido em
        AplicacaoViewSchema.
    """
    return {
        "id"        : aplicacao.id,
        "nome"      : aplicacao.nome,
        "descricao" : aplicacao.descricao,
        "sigla"     : aplicacao.sigla,
        "status"    : aplicacao.status
    }

class AplicacaoViewSchema(BaseModel):
    """ Define como uma aplicação será retornada (aplicacao.py)
    """
    id:         int = 1
    nome:       str = "SAP Success Factor"
    sigla:      str = "SSF"
    descricao:  str = "SAP Success Factor"
    status:     str = "AA"

class AplicacaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id, nome e sigla da aplicação, seguindo a mesma ordem de prioridade para o filtro.
    """
    id:         int = 0
    nome:       str = ""
    sigla:      str = ""
    descricao:  str = ""
    status:     str = ""


class AplicacaoUpdSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de atualização.
    """
    id:         int = 1
    nome:       Optional[str] = "SAP Success Factor"
    sigla:      Optional[str] = "SSF"
    descricao:  Optional[str] = "SAP Success Factor"
    status:     Optional[str] = "AA"

class AplicacaoDltSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de atualização.
    """
    id:     int = 0
    nome:   str = ""