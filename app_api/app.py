from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

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
    
@app.get('/aplicacao', tags=[aplicacao_tag],
         responses={"200":AplicacaoSchema, "404": ErrorSchema})
def get_produto(query: AplicacaoBuscaSchema):
    """ Faz a busca por uma Aplicação a partir do id do produto
        Retorna uma representação das aplicações
    """ 
    aplicacao_id = query.id
    aplicacao_nome = unquote(unquote(query.nome))
    logger.debug(f"Coletando dados sobre produto #{aplicacao_id}")
    # criando conexão com a base
    session = Session()

    # Fazendo a busca
    if aplicacao_id:
        aplicacao = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).first()
    else:
        aplicacao = session.query(Aplicacao).filter(Aplicacao.nome == aplicacao_nome).first()

    if not aplicacao:
        # Se a aplicação não foi encontrado
        error_msg = "Aplicação não encontrado na base :/"
        logger.warning(f"Erro ao buscar a aplicação '{aplicacao_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Aplicação encontrado: '{aplicacao.nome}'")
        # retorna a representação da aplicação
        return apresenta_aplicacao(aplicacao), 200

@app.delete('/aplicacao', tags=[aplicacao_tag],
            responses={"200":AplicacaoDelSchema, "404": ErrorSchema})
def del_aplicacao(query: AplicacaoBuscaSchema):
    """Deleta uma aplicação a partir do nome da aplicação informado
    
    Retorna uma mensagem de configuração da remoção
    """
    aplicacao_nome = unquote(unquote(query.nome))
    print(aplicacao_nome)
    logger.debug(f"Deletando dados sobre a aplicação #{aplicacao_nome}")
    # Criando conexão com a base
    session = Session()
    # Fazendo a remoção
    count = session.query(Aplicacao).filter(Aplicacao.nome == aplicacao_nome).delete()
    session.commit()

    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando aplicação #{aplicacao_nome}")
        return {"message": "Aplicação removido", "id":aplicacao_nome}
    else:
        # Se a aplicação não foi encontrado
        erro_msg = "Aplicação não encontrada na base :/"
        logger.warning(f"Erro ao deletar a aplicação #'{aplicacao_nome}', {erro_msg}")
        return {"message": erro_msg}, 404

@app.put('/aplicacao', tags=[aplicacao_tag],
         responses={"200": AplicacaoSchema, "404" : ErrorSchema})
def upd_aplicacao(query: AplicacaoUpdSchema):
    """Atualiza uma aplicação a partir do ID da aplicação informado
    
    Retorna uma mensagem de configuração da remoção
    """
    aplicacao_nome = unquote(unquote(query.nome))
    aplicacao_id = query.id
    print(aplicacao_nome)
    
    if not aplicacao_nome or aplicacao_nome == "":
        # Se não foi informado nenhum nome
        error_msg = "Nome da aplicação na base não pode ficar em branco:/"
        logger.warning(f"Erro ao atualizar o nome da aplicação '{aplicacao_id}', {error_msg}")
        return {"message": error_msg}, 404

    
    print(aplicacao_nome, "ID: ",aplicacao_id)
    logger.debug(f"Atualizando dados sobre a aplicação #{aplicacao_nome}")

    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    obj_id = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).first()
    if not obj_id:
        # Se a aplicação não foi encontrado
        error_msg = "Aplicação não encontrada na base :/"
        logger.warning(f"Erro ao buscar a aplicação '{aplicacao_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        # Montando a query para atualização do nome
        stmt = (update(Aplicacao)
            .where(Aplicacao.id == obj_id.id)
            .values(nome=aplicacao_nome))
        print(stmt)
        # Executando a atualização
        session.execute(stmt)
        # Gravando a atualização
        session.commit()

        if obj_id:
            # Retorna a representação da mensagem de confirmação
            logger.debug(f"Alterando a aplicação #{aplicacao_nome}")
            return {"message": "Aplicação atualizada ", "id":aplicacao_id}

