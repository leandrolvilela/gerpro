/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/aplicacoes';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.aplicacoes.forEach(item => insertList(item.id, item.nome, item.sigla, item.descricao, item.status))
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
      insertList(id, nome, sigla, descricao, status);
      limparFormulario()
    })
    .catch((error) => {
      console.error('Error:', error);
    });
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
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = () => {
  let inputProduct = document.getElementById("newInput").value;
  let inputQuantity = document.getElementById("newQuantity").value;
  let inputPrice = document.getElementById("newPrice").value;

  if (inputProduct === '') {
    alert("Escreva o nome de um item!");
  } else if (isNaN(inputQuantity) || isNaN(inputPrice)) {
    alert("Quantidade e valor precisam ser números!");
  } else {
    insertList(inputProduct, inputQuantity, inputPrice)
    postItem(inputProduct, inputQuantity, inputPrice)
    alert("Item adicionado!")
  }
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

// Função para confirmar a exclusão
const confirmDelete = (id) => {
  var appNome = 'row_'+id+"_1";
  var celValue = document.getElementById(appNome).textContent;
  // var celValue = cel.textContent
  let msg = "Tem certeza que deseja excluir o app "+ id +" - "+celValue+" ?";
  if (confirm(msg)) {
      deleteItem(id);
  }
}

function editItem(appId, appNome, appSigla, appDescricao, appStatus){

  data = {
    id:         appId,
    nome:       appNome,
    sigla:      appSigla,
    descricao:  appDescricao,
    status:     appStatus
  };

  let url = 'http://127.0.0.1:5000/aplicacao';
  fetch(url, {
    method: 'PUT',
    headers:{
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then((response) => {
      console.log('Retornou: ', response)
      limpaTabela()
      limparFormulario()
      getList()
      $('#myModal').modal('hide');
    })
    .catch((error) => {
      console.error('Error:', error);
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

  let url, filtro = '';

  if (nome) {
    filtro = "nome=" + encodeURIComponent(nome) + '&';
  }
  if (sigla) {
    filtro += "sigla=" + encodeURIComponent(sigla) + '&'
  }
  if (descricao) {
    filtro += "descricao=" + encodeURIComponent(descricao) + '&'
  }
  if (status) {
    filtro += "status=" + encodeURIComponent(status) + '&'
  }

  if (filtro) {
    url = 'http://127.0.0.1:5000/aplicacao?' + filtro;
  } else {
    url = 'http://127.0.0.1:5000/aplicacoes';
  }

  // fecharMensagemErro();

  fetch(url, {
    method: 'GET'
  })
    .then((response) => response.json())
    .then((data) => {

      limpaTabela();
      fecharMensagemErro();
      
      if (data.message){
        exibeErro(data.message)
      } else { 
        if (data && data.aplicacoes) {
          data.aplicacoes.forEach(item => insertList(item.id, item.nome, item.sigla, item.descricao, item.status))
        }
        else if (data) {
          insertList(data.id, data.nome, data.sigla, data.descricao, data.status);
        }
      }

    })
    .catch((error) => {
      console.error('Error filtro:', error);
      exibeErro(error.message)
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