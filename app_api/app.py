from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import lazyload

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
        nome      = form.nome,
        sigla     = form.sigla,
        status    = form.status,
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
        error_msg = f"Aplicação de mesmo nome e/ou sigla já salvo na base ( {repr(e)} )"
        logger.warning(f"Erro ao adicionar a aplicação '{aplicacao.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível salva novo item ( {repr(e)} )"
        logger.warning(f"Erro ao adicionar a aplicação '{aplicacao.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    
    
@app.get('/aplicacoes', tags=[aplicacao_tag],
         responses={"200": ListagemAplicacoesSchema, "404": ErrorSchema})
def get_aplicacoes():
    """Faz a busca por todas as Aplicações cadastradas

    Retorna uma representação da listagem de aplicações.
    """
    logger.debug(f"Coletando aplicações ")

    # criando conexão com a base
    session = Session()
    
    # fazendo a busca
    aplicacoes = session.query(Aplicacao).all()
    
    if not aplicacoes:
        # se não há aplicações cadastradas
        return {"aplicacoes": []}, 200
    else:
        logger.debug(f"Aplicações econtradas {len(aplicacoes)}")
        # retorna a representação de produto
        return apresenta_aplicacoes(aplicacoes), 200
    

@app.get('/aplicacao', tags=[aplicacao_tag],
         responses={"200":AplicacaoSchema, "404": ErrorSchema})
def get_aplicacao(query: AplicacaoBuscaSchema):
    """ Faz a busca por uma Aplicação a partir do id do produto
        Retorna uma representação das aplicações
    """ 
    aplicacao_id = query.id
    aplicacao_nome = unquote(unquote(query.nome))
    aplicacao_sigla = unquote(unquote(query.sigla))
    logger.debug(f"Coletando dados sobre a aplicação #{aplicacao_id}")
    # criando conexão com a base
    session = Session()

    # Fazendo a busca
    if aplicacao_id:
        aplicacao = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).first()
    else:
        if aplicacao_nome:
            aplicacao = session.query(Aplicacao).filter(Aplicacao.nome == aplicacao_nome).first()
        else:
            aplicacao = session.query(Aplicacao).filter(Aplicacao.sigla == aplicacao_sigla).first()

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
def del_aplicacao(query: AplicacaoDltSchema):
    """Deleta uma aplicação a partir do nome da aplicação informado
    
    Retorna uma mensagem de configuração da remoção
    """

    aplicacao_nome  = unquote(unquote(query.nome))
    aplicacao_id    = query.id
    
    # print(f" APLICACAO: {aplicacao_nome} ID: {aplicacao_id}")
    logger.debug(f"Deletando dados sobre a aplicação #{aplicacao_id}-{aplicacao_nome}")
    
    # Criando conexão com a base
    session = Session()

    if aplicacao_id and aplicacao_nome:
        # Fazendo a remoção pelo id da aplicação e nome
        count = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id and Aplicacao.nome == aplicacao_nome).delete()
    else:
        if aplicacao_id:
            # Fazendo a remoção pelo id da aplicação
            count = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).delete()
        else:
            # Fazendo a remoção pelo nome da aplicação
            count = session.query(Aplicacao).filter(Aplicacao.nome == aplicacao_nome).delete()

    session.commit()
    # print(count)
    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando aplicação #{aplicacao_nome}.")
        return {"message": "Aplicação removida", "id":aplicacao_nome}
    
    else:
        # Se a aplicação não foi encontrado
        erro_msg = "Aplicação não encontrada na base :/"
        logger.warning(f"Erro ao deletar a aplicação id {aplicacao_id} #'{aplicacao_nome}', {erro_msg}")
        return {"message": erro_msg}, 404


# Definição da função que verifica se os campos foram alterados
def upd_campo_modificados(campo, novo_valor):
    if novo_valor is not None and novo_valor != "" and campo != novo_valor:
        return novo_valor

    return campo  


@app.before_request
def before_request():
    if request.content_type == 'application/json':
        request.json_data = request.get_json()


@app.put('/aplicacao', tags=[aplicacao_tag],
         responses={"200": AplicacaoSchema, "404" : ErrorSchema})
def upd_aplicacao(query: AplicacaoUpdSchema):
    """Atualiza uma aplicação a partir do ID da aplicação informado
    
    Retorna uma mensagem de configuração da remoção
    """
    query = request.json_data

    aplicacao_id        = query['id']
    aplicacao_nome      = unquote(unquote(query['nome']))
    aplicacao_sigla     = unquote(unquote(query['sigla']))
    aplicacao_descricao = unquote(unquote(query['descricao']))
    aplicacao_status    = unquote(unquote(query['status']))

    print(aplicacao_nome)
    
    if not aplicacao_nome or aplicacao_nome == "":
        # Se não foi informado nenhum nome
        error_msg = "Nome da aplicação na base não pode ficar em branco:/"
        logger.warning(f"Erro ao atualizar o nome da aplicação '{aplicacao_id}', {error_msg}")
        return {"message": error_msg}, 404
    
    #print(aplicacao_nome, "ID: ",aplicacao_id)
    logger.debug(f"Atualizando dados sobre a aplicação #{aplicacao_nome}")

    # Criando conexão com a base
    session = Session()

    try:
        # Fazendo a busca pelo ID da aplicação
        db_aplicacao = session.query(Aplicacao).filter(Aplicacao.id == aplicacao_id).first()
        
        if not db_aplicacao:
            # Se a aplicação não foi encontrado
            error_msg = f"Aplicação não encontrada na base. Detalhe: {repr(e)}"
            logger.warning(f"Erro ao buscar a aplicação '{aplicacao_id}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            db_aplicacao.nome      = upd_campo_modificados(db_aplicacao.nome, aplicacao_nome)
            db_aplicacao.sigla     = upd_campo_modificados(db_aplicacao.sigla, aplicacao_sigla)
            db_aplicacao.descricao = upd_campo_modificados(db_aplicacao.descricao, aplicacao_descricao)
            db_aplicacao.status    = upd_campo_modificados(db_aplicacao.status, aplicacao_status)


            msg = f"Nome: {db_aplicacao.nome}, Sigla: {db_aplicacao.sigla}, Descrição: {db_aplicacao.descricao}"
            print(msg)

            # Grava alteração
            session.add(db_aplicacao)

            # Gravando a atualização
            session.commit()

            logger.debug(f"Editado Aplicação de nome: '{db_aplicacao.nome}'")
            return apresenta_aplicacao(db_aplicacao), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível salvar novo item . Detalhe: {repr(e)}"
        logger.warning(f"Erro ao adicionar aplicação '{db_aplicacao.nome}', {error_msg}")
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
    
    # print(f"Descrição: {tecnologia.descricao}, Status: {tecnologia.status}, \n" \
    #   f"Tipo Tecnologia: {tecnologia.tipo_tecnologia}, Versão: {tecnologia.ultima_versao}")
    
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

@app.get('/tecnologias', tags=[tecnologia_tag],
         responses={"200": ListagemTecnologiaSchema, "404": ErrorSchema})
def get_tecnologias():
    """Faz a busca por todas as tecnologias cadastradas

    Retorna uma representação da listagem de tecnologias.
    """
    logger.debug(f"Coletando tecnologias")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tecnologias = session.query(Tecnologia).all()

    if not tecnologias:
        # se não há tecnologias cadastradas
        return {"tecnologias": []}, 200
    else:
        logger.debug(f"tecnologias econtrados {len(tecnologias)}")
        # retorna a representação de produto
        return apresenta_tecnologias(tecnologias), 200


@app.get('/tecnologia', tags=[tecnologia_tag],
         responses={"200":TecnologiaSchema, "404": ErrorSchema})
def get_tecnologia(query: TecnologiaBuscaSchema):
    """ Faz a busca por uma Tecnologia a partir do id do produto e tipo de tecnologia
        Retorna uma representação das aplicações
    """ 
    tecnologia_id = query.id
    tecnologia_descricao = unquote(unquote(query.descricao))
    
    logger.debug(f"Coletando dados sobre a tecnologia #{tecnologia_id}")

    # criando conexão com a base
    session = Session()

    # Fazendo a busca
    if tecnologia_id:
        tecnologia = session.query(Tecnologia).filter(Tecnologia.id == tecnologia_id).first()
    else:
        tecnologia = session.query(Tecnologia).filter(Tecnologia.descricao == tecnologia_descricao).first()
        
    if not tecnologia:
        # Se a Tecnologia não foi encontrado
        error_msg = "Tecnologia não encontrada na base :/"
        logger.warning(f"Erro ao buscar a aplicação '{tecnologia_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Tecnologia encontrada: '{tecnologia.descricao}'")
        # retorna a representação da Tecnologia
        return apresenta_tecnologia(tecnologia), 200


@app.delete('/tecnologia', tags=[tecnologia_tag],
            responses={"200":TecnologiaDelSchema, "404": ErrorSchema})
def del_tecnologia(query: TecnologiaBuscaSchema):
    """Deleta uma aplicação a partir do nome da tecnologia informado
    
    Retorna uma mensagem de configuração da remoção
    """
    tecnologia_id         = query.id
    tecnologia_descricao  = unquote(unquote(query.descricao))
        
    # print(f" TECNOLOGIA: {tecnologia_descricao} ID: {tecnologia_id}")
    logger.debug(f"Deletando dados sobre a tecnologia #{tecnologia_id}-{tecnologia_descricao}")
    
    # Criando conexão com a base
    session = Session()

    if tecnologia_id and tecnologia_descricao:
        # Fazendo a remoção pelo id da tecnologia e descricao
        count = session.query(Tecnologia).filter(Tecnologia.id == tecnologia_id and Tecnologia.descricao == tecnologia_descricao).delete()
    else:
        if tecnologia_id:
            # Fazendo a remoção pelo id da tecnologia
            count = session.query(Tecnologia).filter(Tecnologia.id == tecnologia_id).delete()
        else:
            # Fazendo a remoção pelo descrição da tecnologia
            count = session.query(Tecnologia).filter(Tecnologia.descricao == tecnologia_descricao).delete()

    session.commit()
    # print(count)
    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando tecnologia #{tecnologia_descricao}.")
        return {"message": "Tecnologia removida", "id":tecnologia_descricao}
    
    else:
        # Se a tecnologia não foi encontrado
        erro_msg = "Tecnologia não encontrada na base :/"
        logger.warning(f"Erro ao deletar a tecnologia id {tecnologia_id} #'{tecnologia_descricao}', {erro_msg}")
        return {"message": erro_msg}, 404


@app.put('/tecnologia', tags=[tecnologia_tag],
         responses={"200": TecnologiaSchema, "404" : ErrorSchema})
def upd_tecnologia(query: TecnologiaUpdSchema):
    """Atualiza uma tecnologia a partir do ID da tecnologia informado
    
    Retorna uma mensagem de configuração da remoção
    """
    tecnologia_id        = query.id
    tecnologia_descricao = unquote(unquote(query.descricao))
    tecnologia_tipo      = query.tipo_tecnologia
    tecnologia_status    = query.status
    tecnologia_versao    = query.ultima_versao

    if not tecnologia_descricao or tecnologia_descricao == "":
        # Se não foi informado nenhum nome
        error_msg = "Nome da tecnologia na base não pode ficar em branco:/"
        logger.warning(f"Erro ao atualizar o nome da tecnologia '{tecnologia_id}', {error_msg}")
        return {"message": error_msg}, 404
    
    #print(aplicacao_nome, "ID: ",aplicacao_id)
    logger.debug(f"Atualizando dados sobre a tecnologia #{tecnologia_descricao}")

    # Criando conexão com a base
    session = Session()

    try:
        # Fazendo a busca pelo ID da tecnologia
        db_tecnologia = session.query(Tecnologia).filter(Tecnologia.id == tecnologia_id).first()
        
        if not db_tecnologia:
            # Se a tecnologia não foi encontrado
            error_msg = f"Tecnologia não encontrada na base. Detalhe: {repr(e)}"
            logger.warning(f"Erro ao buscar a tecnologia '{tecnologia_id}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            db_tecnologia.descricao       = upd_campo_modificados(db_tecnologia.descricao, tecnologia_descricao)
            db_tecnologia.tipo_tecnologia = upd_campo_modificados(db_tecnologia.tipo_tecnologia, tecnologia_tipo)
            db_tecnologia.status          = upd_campo_modificados(db_tecnologia.status, tecnologia_status)
            db_tecnologia.ultima_versao   = upd_campo_modificados(db_tecnologia.ultima_versao, tecnologia_versao)

            # Grava alteração
            session.add(db_tecnologia)

            # Gravando a atualização
            session.commit()

            logger.debug(f"Editado descrição da tecnologia: '{db_tecnologia.descricao}'")
            return apresenta_tecnologia(db_tecnologia), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = f"Não foi possível salvar novo item . Detalhe: {repr(e)}"
        logger.warning(f"Erro ao adicionar tecnologia '{db_tecnologia.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400
