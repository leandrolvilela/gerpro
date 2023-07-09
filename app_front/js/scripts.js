/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async (page, perPage) => {
  //let url = 'http://127.0.0.1:5000/aplicacoes?page=${page}';
  let url = `http://127.0.0.1:5000/aplicacoes?page=${page}&per_page=${perPage}`;
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.aplicacoes.forEach(item => 
        insertList(item.id, item.nome, item.sigla, item.descricao, item.status));
      
        // const totalPages   = data.totalPages;
        // const itemsPerPage = data.itemsPerPage; //Quantidade de itens por página
        // const page         = data.currentPage;

        // generatePagination(totalPages, itemsPerPage, page);

    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/

getList()


/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postApp = async (nome, sigla, descricao, status) => {

console.log("NOME: ",nome," SIGLA: ",sigla," DESCRICAO: ",descricao)

  const formData = new FormData();
  formData.append('nome', nome);
  formData.append('sigla', sigla);
  formData.append('descricao', descricao);
  formData.append('status', status);

  let url = 'http://127.0.0.1:5000/aplicacao';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .then((data)=>{
      const id        = data.id;
      const nome      = data.nome;
      const sigla     = data.sigla;
      const descricao = data.descricao;
      const status    = data.status;
      const msg       = data.message;

      console.log("ID: ", id, " NOME: ",nome, " SIGLA: ", sigla, " MSG: ",msg)

      if (msg){
        var titulo_msg = 'Erro ao cadastrar!'
        // Exibe mensagem de erro
        exibeMsgErro(titulo_msg, msg)
      } else {
        insertList(id, nome, sigla, descricao, status);
        limparFormulario()
      }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function exibeMsgErro(titulo_msg, msg){
  const divMsgErro = document.getElementById('msgErroCadastro');
  divMsgErro.style.display = 'list-item';
  const strongElement = document.querySelector('#msgErroCadastro strong');
  strongElement.innerHTML = titulo_msg;
  const pElement = document.querySelector('#msgErroCadastro p');
  pElement.innerHTML = msg;
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  let url = 'http://127.0.0.1:5000/aplicacao?id=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => {
      if (response.ok) {
        // Exclusão bem-sucedida, remover a linha da tabela
        var rowId = 'row_' + item;  // ID da linha a ser removida
        var row = document.getElementById(rowId);
        if (row) {
          row.remove()
        }
      }
      return response.json();
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (id, nome, sigla, descricao, status) => {

  /** Cria botão de edição de aplicação */
  var editBtn = document.createElement('button');
  editBtn.setAttribute('type', 'button');
  editBtn.setAttribute('onclick', 'preencheFormulario("' + id + '")');
  editBtn.classList.add('btn');
  editBtn.innerHTML = '<i class="icon-edit"></i>';

  /** Cria botão de exclusão de aplicação */
  var delBtn = document.createElement('button');
  delBtn.setAttribute('type', 'submit');
  delBtn.setAttribute('onclick', 'confirmDelete("' + id + '")');
  delBtn.classList.add('btn');
  delBtn.innerHTML = '<i class="icon-trash"></i>';

  /** Cria a tabela */
  var item = [id, nome, sigla, descricao, status]

  /** Adiciona os botões de edição e exclusão na tabela */
  item.push(editBtn);
  item.push(delBtn);
  
  var table = document.getElementById('myTable').getElementsByTagName('tbody')[0];
  var row = table.insertRow();
  var rowId = 'row_' + id;

  /** Atribui o ID á linha */
  row.setAttribute('id', rowId)

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);

    cel.setAttribute('id', rowId + '_' + i)

    if (typeof item[i] === 'object') {
      cel.appendChild(item[i]);           // Insere os botões
    } else {
      cel.textContent = item[i];          // Insere o conteudo nas tabelas
    }
  }

}


const generatePagination = (totalPages, itemsPerPage, currentPage) => {
  
  // console.log(itemsPerPage, " - ",currentPage, " Total Pages: ",totalPages)

  const paginationList = document.querySelector('.pagination-list');
  paginationList.innerHTML = ''; //limpar o conteúdo anterior do elemento antes de adicionar os novos elementos de paginação
  
  const pagination = document.createElement('ul');
  pagination.classList.add('pagination');

  for (let i = 1; i <= totalPages; i++) {
    const li = document.createElement('li');
    li.classList.add('page-item');

    const link = document.createElement('a');
    link.classList.add('page-link');
    link.href = '#';
    link.textContent = i;

    if (i === currentPage) {
      li.classList.add('active');
    }

    link.addEventListener('click', () => {
      limpaTabela();
      getList(i, itemsPerPage);
    });

    li.appendChild(link);
    pagination.appendChild(li);
  }

  paginationList.appendChild(pagination);
};




// Função para confirmar a exclusão
const confirmDelete = (id) => {

  /* Como está configurado os IDs da tabela
    O id da coluna row_id_0 = ID 
    O id da coluna row_id_1 = NOME DA APLICAÇÃO (*)
    O id da coluna row_id_2 = SIGLA 
    O id da coluna row_id_3 = DESCRIÇÃO 
    O id da coluna row_id_4 = STATUS 
    O id da coluna row_id_5 = BOTÃO DE EDIÇÃO 
    O id da coluna row_id_6 = BOTÃO DE EXCLUSÃO 
  */

  // Recupera o Nome da Aplicação pelo ID (*)
  var appNome = 'row_' + id + "_1";

  // Recupera o nome da aplicação que está na tabela
  var celValue = document.getElementById(appNome).textContent;

  // Configura mensagem que irá exibir na tela de confirmação de exclusão
  let confirmMessage = document.getElementById('confirmMessage');
  confirmMessage.textContent = `Tem certeza que deseja excluir o app ${id} - ${celValue} ?`;
  
  // adiciona a função no botão com o ID a ser excluido
  let idBtn  = document.getElementById('btnConfirmDelete');
  let funDel = 'deleteItemConfirmed('+id+')';
  idBtn.setAttribute('onclick', funDel);

  // Exibe tela de confirmação
  $('#confirmModal').modal('show');

}

// Função para executar a exclusão após a confirmação
const deleteItemConfirmed = (id) => {

  // Realize a exclusão do item
  deleteItem(id)
  
  // Feche o modal de confirmação
  $('#confirmModal').modal('hide');

}

function editItem(appId, appNome, appSigla, appDescricao, appStatus){

  data = {
    id:         appId,
    nome:       appNome,
    sigla:      appSigla,
    descricao:  appDescricao,
    status:     appStatus
  };

  // console.log('JSON: ', JSON.stringify(data));
  // console.log('Data:', data)

  let url = 'http://127.0.0.1:5000/aplicacao';
  fetch(url, {
    method: 'PUT',
    headers:{
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then((response) => {
      if (response.ok){

        limpaTabela()
        limparFormulario()
        getList()
        $('#myModal').modal('hide');

      } else{

        // Requisição com erro, capturar mensagem de erro
        return response.json().then((data) => {
          const errorMessage = data.message;
          // console.error('Erro:', errorMessage);
          const titulo_msg = 'Erro ao atualizar!'

          // Exibe mensagem de erro
          exibeMsgErro(titulo_msg, errorMessage)

        });

      }
    })
    .catch((error) => {
      console.error('Error:', error.message);
    });
}

function preencheFormulario(id){

  /** RECUPERA VALORES DA APLICAÇÃO QUE ESTÁ NA TABELA QUE O USUÁRIO CLICOU */

  // Recupera nome do app da tabela
  var idNome  = 'row_'+id+"_1";
  var celNome = document.getElementById(idNome);
  var appNome = celNome.textContent

  // Recupera sigla do app da tabela
  var idSigla = 'row_'+id+"_2";
  var celSigla = document.getElementById(idSigla);
  var appSigla = celSigla.textContent

  // Recupera descrição do app da tabela
  var idDescricao  = 'row_'+id+"_3";
  var celDescricao = document.getElementById(idDescricao);
  var appDescricao = celDescricao.textContent

  // Recupera status do app da tabela
  var idStatus  = 'row_'+id+"_4";
  var celStatus = document.getElementById(idStatus);
  var appStatus = celStatus.textContent  

  /** PREENCHE OS VALORES DA APLICAÇÃO NO FORMULARIO */

  // Obtém o elemento do modal pelo ID
  var modalElement = document.getElementById('myModal');

  // Exibe o formulário
  $(modalElement).modal('show');

  // preenche o ID da aplicação em um input hidden
  document.getElementById('cadAppId').value             = id;
  document.getElementById("cadAppNome").value           = appNome;
  document.getElementById("cadAppSigla").value          = appSigla;
  document.getElementById("cadAppDescricao").value      = appDescricao;
  document.getElementById("cadAppStatus").selectedIndex = appStatus;
  document.getElementById("myModalLabel").textContent   = "Alteração de Aplicação"
}

function cadastrarApp(nome, sigla, descricao, status) {
  postApp(nome, sigla, descricao, status)
}



function filtrarRegistros(nome, sigla, descricao, status) {

  const formData = new FormData();
  formData.append('nome', nome);
  formData.append('sigla', sigla);
  formData.append('descricao', descricao);
  formData.append('status', status);

  let url = 'http://127.0.0.1:5000/aplicacao_filtros';
  fetch(url, {
    method: 'POST',
    body: formData
  })
    .then((response) => response.json())
    .then((data)=>{
      limpaTabela()
      data.aplicacoes.forEach(item => insertList(item.id, item.nome, item.sigla, item.descricao, item.status))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function exibeErro(msgErro){
  const errorMessage = document.getElementById('error-message');
  const errorText = document.getElementById('error-text');
  errorText.textContent = msgErro;
  errorMessage.style.display = 'block';
}

function limpaTabela(){
  var tableBody = document.getElementById('myTable').getElementsByTagName('tbody')[0];
  tableBody.innerHTML = ''; // Limpa o conteúdo da tabela
}

function limparFormulario() {
  document.getElementById('cadAppId').value = 0;
  document.getElementById("cadAppNome").value = "";
  document.getElementById("cadAppSigla").value = "";
  document.getElementById("cadAppDescricao").value = "";
  document.getElementById("cadAppStatus").selectedIndex = 0; // Define o primeiro item como selecionado
  document.getElementById("myModalLabel").textContent   = "Cadastro de Aplicação"
}

function fecharMensagemErro() {
  const errorMessage = document.getElementById('error-message');
  const errorText = document.getElementById('error-text');
  errorText.textContent = '';
  errorMessage.style.display = 'none';
}