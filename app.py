# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Author:      Elder Sanitá Trevisan
#
# Copyright(©) 2016 Elder Sanitá Trevisan
# Licence:     GPL
#------------------------------------------------------------------------------
from bottle import redirect, route, static_file, error, request, run,\
	jinja2_template as template
import os
import html
import model
import re

BASEDIR = os.path.dirname(__file__)
BANCO = os.path.join(BASEDIR, 'agenda.db')


@route('/')
@route('/index')
def index():
	contatos = model.ler_todos_contatos()
	return template("index.html", data=contatos)

@route('/criar_contato', method=['GET', 'POST'])
def criar_contato():
	if request.method == 'POST':
		nome = html.escape(request.forms.get('nome'))
		telefone = html.escape(request.forms.get('telefone'))
		telefone = re.sub(r'\D', "", telefone)
		logradouro = html.escape(request.forms.get('logradouro'))
		numero = html.escape(request.forms.get('numero'))
		numero = re.sub(r'\D', "", numero)
		complemento = html.escape(request.forms.get('complemento'))
		bairro = html.escape(request.forms.get('bairro'))
		cidade = html.escape(request.forms.get('cidade'))
		uf = html.escape(request.forms.get('uf'))
		
		d = model.inserir_contato(nome, telefone, logradouro, numero,\
		complemento, bairro, cidade, uf)
		
		if d != None:
			return "<script>alert('",d,"'); window.history.back();</script>"
		else:
			redirect('/')
	else:
		return template('criar_contato.html')

@route('/contato/<pk:int>', method='GET')
def contato(pk):
	pk = int(pk)
	contato = model.ler_contato(pk)
	return template('contato.html', data=contato)
	
@route('/contato/edita_contato/<pk:int>', method=['GET','POST'])
def edita_contato(pk):
	pk = int(pk)
	if request.method == 'POST':
		nome = html.escape(request.forms.get('nome'))
		telefone = html.escape(request.forms.get('telefone'))
		telefone = re.sub(r'\D', "", telefone)
		logradouro = html.escape(request.forms.get('logradouro'))
		numero = html.escape(request.forms.get('numero'))
		numero = re.sub(r'\D', "", numero)
		complemento = html.escape(request.forms.get('complemento'))
		bairro = html.escape(request.forms.get('bairro'))
		cidade = html.escape(request.forms.get('cidade'))
		uf = html.escape(request.forms.get('uf'))
		
		d = model.editar_contato(nome, telefone, logradouro, numero,\
		complemento, bairro, cidade, uf, pk)
		
		if d != None:
			return "<script>alert('",d,"'); window.history.back();</script>"
		else:
			redirect('/')
	else:
		return template('criar_contato.html')
	
@route('/contato/exclui_contato/<pk:int>')
def exclui_contato(pk):
	pk = int(pk)
	model.excluir_contato(pk)
	redirect('/')

@route('/static/<filename:path>')
def server_static(filename):
	return static_file(filename, root='static/')
	
@error(404)
def error404(error):
	return "Ops, página não encontrada!"


if __name__ == "__main__":
	run(reloader=True, debug=True)
