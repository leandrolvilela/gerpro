from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

app_tech = Table(
    "app_tech",
    Base.metadata,
    Column("id_app", ForeignKey("aplicacao.pk_aplicacao"), primary_key=True),
    Column("id_tech", ForeignKey("tecnologia.pk_tecnologia"), primary_key=True),
    Column("versao",String(50))
)