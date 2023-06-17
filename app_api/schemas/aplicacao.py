from pydantic import BaseModel
from typing import Optional, List
from model.aplicacao import Aplicacao

from schemas import ComentarioSchema

class AplicacaoSchema(BaseModel):
    """ Define uma nova aplicação a ser inserida deve ser representada
    """
    nome: str = "SAP Success Factor"
    sigla: str = "SSF"
    descricao: str = "O SAP SuccessFactors é uma solução completa para um RH estratégico e eficaz."
    status: str = "AA"


def apresenta_aplicacoes(aplicacoes: List[Aplicacao]):
    """ Retorna uma representação da aplicação seguindo o schema definido em
        AplicaçãoViewSchema.
    """
    result = []
    for aplicacao in aplicacoes:
        result.append({
            "nome"      : aplicacao.nome,
            "descricao" : aplicacao.descricao,
            "sigla"     : aplicacao.sigla,
            "status"    : aplicacao.status,
        })

    return {"aplicacoes": result}

def apresenta_aplicacao(aplicacao: Aplicacao):
    """ Retorna uma representação da aplicacao seguindo o schema definido em
        AplicacaoViewSchema.
    """
    return {
        "nome"      : aplicacao.nome,
        "descricao" : aplicacao.descricao,
        "sigla"     : aplicacao.sigla,
        "status"    : aplicacao.status
    }

def AlicacaoViewSchema(BaselModel):
    """ Define como uma aplicação será retornada
    """
    id: int=1
    nome: str="SAP Success Factor"
    sigla: str="SSF"
    descricao: str="SAP Success Factor"
    status: str="AA"

class AplicacaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str