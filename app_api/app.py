from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Aplicacao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Gerenciamento de Aplicações", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description=" Seleção de documentação: Swagger, Redoc ou RapiDoc")
aplicacao_tag = Tag(name="Aplicacao", description="Adição, visualização e remoção de aplicações à base")
#comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/aplicacao', tags=[aplicacao_tag])
def add_aplicacao(form: AplicacaoSchema):
    aplicacao = Aplicacao(
        nome=form.nome,
        sigla=form.sigla,
        status=form.status,
        descricao=form.descricao
    )
    logger.debug(f"Adicionando aplicação de nome: '{aplicacao.nome}'")
