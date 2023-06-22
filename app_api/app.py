from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
# from sqlalchemy import update

from model import Session, Aplicacao, Tecnologia
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Gerenciamento de Aplicações", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description=" Seleção de documentação: Swagger, Redoc ou RapiDoc")
aplicacao_tag = Tag(name="Aplicação", description="Adição, visualização e remoção de aplicações à base")
tecnologia_tag = Tag(name="Tecnologia", description="Adição, visualização e remoção de aplicações à base")
#comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# -------------------------------
# METODOS REFERENTE A APLICAÇÃO
# -------------------------------

@app.post('/aplicacao', tags=[aplicacao_tag],
          responses={"200":AplicacaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_aplicacao(form:AplicacaoSchema):
    """Método para adicionar uma nova aplicação na base de dados
    
    Retorna uma representação das aplicações
    """

    aplicacao = Aplicacao(
        nome = form.nome,
        sigla = form.sigla,
        status = form.status,
        descricao = form.descricao
    )
    logger.debug(f"Adicionando aplicação de nome: '{aplicacao.nome}'")
    try:
        # Criando conexao com a base de dados
        session = Session()

        # Adicionando aplicação
        session.add(aplicacao)

        # efetivando o comando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado aplicação de nome: '{aplicacao.nome}'")
        return apresenta_aplicacao(aplicacao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = f"Aplicação de mesmo nome já salvo na base ( {repr(e)} )"
        logger.warning(f"Erro ao adicionar a aplicação '{aplicacao.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível salva novo item ( {repr(e)} )"
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
    logger.debug(f"Coletando dados sobre a aplicação #{aplicacao_id}")
    # criando conexão com a base
    session = Session()

    # Fazendo a busca
    if aplicacao_id:
        aplicacao = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).first()
    else:
        aplicacao = session.query(Aplicacao).filter(Aplicacao.nome == aplicacao_nome).first()

    if not aplicacao:
        # Se a aplicação não foi encontrado
        error_msg = "Aplicação não encontrada na base :/"
        logger.warning(f"Erro ao buscar a aplicação '{aplicacao_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Aplicação encontrada: '{aplicacao.nome}'")
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
        return {"message": "Aplicação removida", "id":aplicacao_nome}
    
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
    aplicacao_id   = query.id
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

    try:
        # Fazendo a busca
        db_aplicacao = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).first()
        
        if not db_aplicacao:
            # Se a aplicação não foi encontrado
            error_msg = "Aplicação não encontrada na base :/"
            logger.warning(f"Erro ao buscar a aplicação '{aplicacao_id}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            # Montando a query para atualização do nome
            #stmt = (update(Aplicacao)
            #    .where(Aplicacao.id == obj_id.id)
            #    .values(nome = aplicacao_nome))
            # print(stmt)

            if query.nome:
                db_aplicacao.nome = query.nome

            # Grava alteração
            session.add(db_aplicacao)

            # Executando a atualização
            #session.execute(stmt)

            # Gravando a atualização
            session.commit()

            logger.debug(f"Editado Aplicação de nome: '{db_aplicacao.nome}'")
            return apresenta_aplicacao(db_aplicacao), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{db_aplicacao.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    
# -------------------------------
# METODOS REFERENTE A TECNOLOGIAS
# -------------------------------

@app.post('/tecnologia', tags=[tecnologia_tag],
          responses={"200":TecnologiaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tecnologia(form:TecnologiaSchema):
    """Método para adicionar uma nova tecnologia na base de dados
    
    Retorna uma representação das tecnologias
    """
    tecnologia = Tecnologia(
        descricao       = form.descricao,
        status          = form.status,
        tipo_tecnologia = form.tipo_tecnologia,
        ultima_versao   = form.ultima_versao
    )

    # Criando conexao com a base de dados
    session = Session()
    
    print(f"Descrição: {tecnologia.descricao}, Status: {tecnologia.status}, \n" \
          f"Tipo Tecnologia: {tecnologia.tipo_tecnologia}, Versão: {tecnologia.ultima_versao}")
    
    logger.debug(f"Adicionando tecnologia : '{tecnologia.descricao}'")
    try:
        # Adicionando aplicação
        session.add(tecnologia)

         # efetivando o comando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado tecnologia : '{tecnologia.descricao}'")
        return apresenta_tecnologia(tecnologia), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = f"Aplicação de mesmo nome já salvo na base. Detalhe: {repr(e)}"
        logger.warning(f"Erro ao adicionar a tecnologia '{tecnologia.descricao}', {error_msg}")
        return {"message": error_msg}, 409 
       
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível salva novo item. Detalhe: {repr(e)}"
        logger.warning(f"Erro ao adicionar a tecnologia '{tecnologia.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400
    
