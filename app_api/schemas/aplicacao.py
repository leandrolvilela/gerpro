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