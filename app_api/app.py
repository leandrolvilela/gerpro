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
aplicacao_tag = Tag(name="Aplicação", description="Adição, visualização e remoção de aplicações à base")
#comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/aplicacao', tags=[aplicacao_tag],
          responses={"200":AplicacaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_aplicacao(form:AplicacaoSchema):
    """Método para adicionar uma nova aplicação na base de dados
    
    Retorna uma representação das aplicações
    """
    aplicacao = Aplicacao(
        nome        = form.nome,
        sigla       = form.sigla,
        status      = form.status,
        descricao   = form.descricao
    )
    logger.debug(f"Adicionando aplicação de nome: '{aplicacao.nome}'")
    try:
        # Criando conexao com a base de dados
        session = Session()
        # Adicionando aplicação
        session.add(aplicacao)
        session.commit()
        logger.debug(f"Adicionado aplicação de nome: '{aplicacao.nome}'")
        return apresenta_aplicacoes(aplicacao), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Aplicação de mesmo nome já salvo na base:/"
        logger.warning(f"Erro ao adicionar a aplicação '{aplicacao.nome}', {error_msg}")
        return {"message": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salva novo item :/"
        logger.warning(f"Erro ao adicionar a aplicação '{aplicacao.nome}', {error_msg}")
        return {"mesage": error_msg}, 400