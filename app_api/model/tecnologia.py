from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base
from .app_tech import app_tech

class Tecnologia(Base):
    __tablename__ = 'tecnologia'

    id              = Column("pk_tecnologia", Integer, primary_key=True)
    descricao       = Column(String(200), unique = True)
    status          = Column(String(2), default="A")
    tipo_tecnologia = Column(String(80))
    ultima_versao   = Column(String(50))
    data_insercao   = Column(DateTime, default=datetime.now())

    aplicacoes = relationship("Aplicacao", secondary="app_tech", back_populates="tecnologias")

    def __init__(self,  descricao:str, 
                        status:str, 
                        tipo_tecnologia:str,
                        ultima_versao:str, 
                        data_insercao:Union[DateTime, None] = None):
        """
        Cadastra uma tecnologia

        Arguments:
            descricao: Descrição da aplicação, tem como objetivo de ter um resumo do que a aplicação entrega para os usuário
            status: Status da aplicação. A - Ativo, I - Inativo
            tipo_tecnologia: Tipo de tecnologia, exemplo: Liguagem de programação, Framework, Banco de Dados, etc
            ultima_versao: A mais recente versão da tecnologia
            data_insercao: data de quando a aplicação foi cadastrada
        """

        self.descricao = descricao
        self.status = status
        self.tipo_tecnologia = tipo_tecnologia
        self.ultima_versao = ultima_versao

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao