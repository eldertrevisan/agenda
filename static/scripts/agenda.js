function habilita_campos(form){
	var bt_salvar = document.getElementById("bt_salvar").disabled = false;
	var form_enable = document.getElementsByClassName(form);
	for (var i=0; i < form_enable.length; i++) {
		form_enable[i].disabled = false;
	}
}

function confirma_exclusao(pk){
	var msg = confirm("Deseja realmente excluir este contato?");
	console.log(pk)
	if (msg == true){
		location.href = "/contato/exclui_contato/"+pk;
	}
}