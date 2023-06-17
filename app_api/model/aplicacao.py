from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Aplicacao(Base):
    __tablename__ = 'aplicacao'

    id              = Column("pk_aplicacao", Integer, primary_key=True)
    nome            = Column(String(150), unique=True)
    sigla           = Column(String(6), unique=True)
    descricao       = Column(String(200))
    status          = Column(String(2), default="AA")
    data_insercao   = Column(DateTime, default=datetime.now())

    def __init__(self,  nome:str, 
                        sigla:str, 
                        descricao:str, 
                        status:str,
                        data_insercao:Union[DateTime, None] = None):
        """
        Cadastra uma aplicação

        Arguments:
            nome: Nome da Aplicação.
            sigla: Sigla da aplicação, para facilitar a identificação da aplicação
            descricao: Descrição da aplicação, tem como objetivo de ter um resumo do que a aplicação entrega para os usuário
            status: Status da aplicação. AA - Aguardando aprovação, A - Ativo, I - Inativo
            data_insercao: data de quando a aplicação foi cadastrada
        """

        self.nome       = nome
        self.sigla      = sigla
        self.descricao  = descricao
        self.status     = status

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao