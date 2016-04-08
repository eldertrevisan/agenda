function habilita_campos(form){
	var bt_salvar = document.getElementById("bt_salvar").disabled = false;
	var form_enable = document.getElementsByClassName(form);
	for (var i=0; i < form_enable.length; i++) {
		form_enable[i].disabled = false;
	}
}

function confirma_exclusao(pk){
var msg = confirm("Deseja realmente excluir este contato?");
if (msg == true){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if (xhttp.readyState == 4 && xhttp.status == 200){
			document.getElementById("contato").innerHTML = xhttp.responseText;
		}
	};
	xhttp.open("GET", "/contato/exclui_contato/"+pk, true);
	xhttp.send(pk);
	}
}