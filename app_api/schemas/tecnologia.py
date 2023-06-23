from pydantic import BaseModel
from typing import Optional, List
from model.tecnologia import Tecnologia

class TecnologiaSchema(BaseModel):
    """ Define uma nova tecnologia a ser inserida ou atualizada deve ser representada (tecnologia.py)
    """
    descricao:       str = "JAVA"
    status:          str = "A"
    tipo_tecnologia: str = "Linguagem de Programação"
    ultima_versao:   str = "JDK 17.0"

class TecnologiaViewSchema(BaseModel):
    """ Define como uma tecnologia será retornada (tecnologia.py)
    """
    id: int=1
    descricao: str = "JAVA"
    status: str = "A"
    tipo_tecnologia: str = "Linguagem de Programação"
    ultima_versao: str = "JDK 17.0"

class ListagemTecnologiaSchema(BaseModel):
    """ Define como uma listagem de tecnologia será retornada (tecnologia.py)
    """
    tecnologia:List[TecnologiaSchema]

# As funções da classe do schemas não podem conter espaços iniciais (identação)
# Pois ocorre erro de importação/utilização no app.py
def apresenta_tecnologias(tecnologias: List[Tecnologia]):
    """ Retorna uma representação da tecnologia seguindo o schema definido em
        TecnologiaViewSchema. (tecnologia.py)
    """
    result = []
    for tecnologia in tecnologias:
        result.append({
            "descricao" : tecnologia.descricao,
            "status"    : tecnologia.status,
            "tipo_tecnologia" : tecnologia.tipo_tecnologia,
            "ultima_versao": tecnologia.ultima_versao,
        })
        
    return {"tecnologias": result}

class TecnologiaDelSchema(BaseModel):
    """ Define como deve ser a estrutura de dado retornado após uma requisição de remoção (tecnologia.py)
    """
    mesage: str
    nome: str

def apresenta_tecnologia(tecnologia: Tecnologia):
    """ Retorna uma representação da tecnologia seguindo o schema definido em
        TecnologiaViewSchema.
    """
    return {
        "descricao"         : tecnologia.descricao,
        "status"            : tecnologia.status,
        "tipo_tecnologia"   : tecnologia.tipo_tecnologia,
        "ultima_versao"     : tecnologia.ultima_versao
    }


class TecnologiaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id, descricao e tipo de tecnologia, seguindo a mesma ordem de prioridade para o filtro.
    """
    id: int = 0
    descricao: str = ""
