from pydantic import BaseModel, Field
from typing import Optional, List
from model.aplicacao import Aplicacao


class AplicacaoSchema(BaseModel):
    """ Define uma nova aplicação a ser inserida ou atualizada deve ser representada (aplicacao.py)
    """
    id:         int = 0
    nome:       str = Field("SAP Success Factor", description="Nome da Aplicação")
    sigla:      str = Field("SSF", description="Sigla da aplicação para facilitar a busca")
    descricao:  str = Field("Solução completa para um RH estratégico e eficaz.", description="Descrição da Aplicação")
    status:     str = Field("AA", description="Possiveis valores AA-Aguardando Aprovação, A-Ativo, I-Inativo")

class AplicacaoViewSchema(BaseModel):
    """ Define como uma aplicação será retornada (aplicacao.py)
    """
    id:         int = 0
    nome:       str = Field("SAP Success Factor", description="Nome da Aplicação")
    sigla:      str = Field("SSF", description="Sigla da aplicação para facilitar a busca")
    descricao:  str = Field("Solução completa para um RH estratégico e eficaz.", description="Descrição da Aplicação")
    status:     str = Field("AA", description="Possiveis valores AA-Aguardando Aprovação, A-Ativo, I-Inativo")



class ListagemAplicacoesSchemaPG(BaseModel):
    """ Define como uma listagem de aplicações será retornada por página (aplicacao.py)
    """
    page:        int = Field(default=1, description="Número da página")
    per_page:    int = Field(default=4, description="Quantidade de itens por página")
    total_pages: int = Field(default=1, description="Número total de páginas")

# As funções da classe do schemas não podem conter espaços iniciais (identação)
# Pois ocorre erro de importação/utilização no app.py
def apresenta_aplicacoesPG(aplicacoes: List[Aplicacao], page, per_page, totalPages):
    """ Retorna uma representação da aplicação seguindo o schema definido em
        AplicaçãoViewSchema.
    """
    result = []
    for aplicacao in aplicacoes:
        result.append({
            "id"        : aplicacao.id,
            "nome"      : aplicacao.nome,
            "sigla"     : aplicacao.sigla,
            "descricao" : aplicacao.descricao,
            "status"    : aplicacao.status
        })
        
    return {"aplicacoes"   : result,
            "totalPages"   : totalPages,
            "currentPage"  : page,
            "itemsPerPage" : per_page}


class ListagemAplicacoesSchema(BaseModel):
    """ Define como uma listagem de aplicações será retornada (aplicacao.py)
    """
    aplicacoes:List[AplicacaoSchema]

# As funções da classe do schemas não podem conter espaços iniciais (identação)
# Pois ocorre erro de importação/utilização no app.py
def apresenta_aplicacoes(aplicacoes: List[Aplicacao]):
    """ Retorna uma representação da aplicação seguindo o schema definido em
        AplicaçãoViewSchema. (aplicacao.py)
    """
    result = []
    for aplicacao in aplicacoes:
        result.append({
            "id"        : aplicacao.id,
            "nome"      : aplicacao.nome,
            "sigla"     : aplicacao.sigla,
            "descricao" : aplicacao.descricao,
            "status"    : aplicacao.status
        })
        
    return {"aplicacoes": result}

class AplicacaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura de dado retornado após uma requisição de remoção (aplicacao.py)
    """
    mesage: str
    nome:   str

def apresenta_aplicacao(aplicacao: Aplicacao):
    """ Retorna uma representação da aplicacao seguindo o schema definido em
        AplicacaoViewSchema.
    """
    return {
        "id"        : aplicacao.id,
        "nome"      : aplicacao.nome,
        "descricao" : aplicacao.descricao,
        "sigla"     : aplicacao.sigla,
        "status"    : aplicacao.status
    }

class AplicacaoViewSchema(BaseModel):
    """ Define como uma aplicação será retornada (aplicacao.py)
    """
    id:         int = 1
    nome:       str = Field("SAP Success Factor", description="Nome da Aplicação")
    sigla:      str = Field("SSF", description="Sigla da aplicação para facilitar a busca")
    descricao:  str = Field("Solução completa para um RH estratégico e eficaz.", description="Descrição da Aplicação")
    status:     str = Field("AA", description="Possiveis valores AA-Aguardando Aprovação, A-Ativo, I-Inativo")


class AplicacaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id, nome e sigla da aplicação, seguindo a mesma ordem de prioridade para o filtro.
    """
    id:         int = 0
    nome:       str = ""
    sigla:      str = ""


class AplicacaoUpdSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de atualização.
    """
    id:         int = 1
    nome:       Optional[str] = "SAP Success Factor"
    sigla:      Optional[str] = "SSF"
    descricao:  Optional[str] = "SAP Success Factor"
    status:     Optional[str] = "AA"

class AplicacaoDltSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de atualização.
    """
    id:     int = 0
    nome:   str = ""