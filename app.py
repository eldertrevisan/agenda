# -*- coding: utf-8 -*-
from bottle import redirect, route, static_file, error, run
from bottle import run, request, jinja2_template as template
import os
import sqlite3

dir = os.path.dirname(__file__)
banco = filename = os.path.join(dir, 'agenda.db')

@route('/')
@route('/index')
def index():
	conn = sqlite3.connect(banco)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM agenda")
	result = cursor.fetchall()
	conn.close()
	return template("index.html", data=sorted(result, key=lambda tup: tup[1]))

@route('/criar_contato', method=['GET', 'POST'])
def criar_contato():
	if request.forms.get('save'):
		nome = request.forms.get('nome')
		telefone = request.forms.get('telefone')
		logradouro = request.forms.get('logradouro')
		numero = request.forms.get('numero')
		complemento = request.forms.get('complemento')
		bairro = request.forms.get('bairro')
		cidade = request.forms.get('cidade')
		uf = request.forms.get('uf')
		
		try:
			conn = sqlite3.connect(banco)
			cursor = conn.cursor()
			cursor.execute('''INSERT INTO agenda
							VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
							''', (None, nome, telefone, logradouro, numero,\
							complemento, bairro, cidade, uf))
			conn.commit()
			conn.close()
			redirect('/index')
		except sqlite3.Error as erro:
			if erro.args[0] == "UNIQUE constraint failed: agenda.nome":
				return "<script>alert('Este contato já existe na agenda!')"\
				"</script>", "<script>window.history.back()</script>"
			else:
				return "<p>Ocorreu o seguinte erro: ",erro.args[0]," </p>"
	else:
		return template('criar_contato.html')

@route('/contato/<pk:int>', method='GET')
def contato(pk):
	conn = sqlite3.connect(banco)
	cursor = conn.cursor()
	cursor.execute('''SELECT * FROM agenda WHERE id=?''',(pk,))
	data = cursor.fetchall()
	conn.close()
	return template('contato.html', data=data)
	
@route('/contato/edita_contato/<pk:int>', method=['GET','POST'])
def edita_contato(pk):
	if request.forms.get('save'):
		nome = request.forms.get('nome')
		telefone = request.forms.get('telefone')
		logradouro = request.forms.get('logradouro')
		numero = request.forms.get('numero')
		complemento = request.forms.get('complemento')
		bairro = request.forms.get('bairro')
		cidade = request.forms.get('cidade')
		uf = request.forms.get('uf')
		try:
			conn = sqlite3.connect(banco)
			cursor = conn.cursor()
			cursor.execute('''UPDATE agenda SET nome=?, telefone=?,
			logradouro=?, numero=?, complemento=?, bairro=?, cidade=?, uf=?
			WHERE id=?''',(nome, telefone, logradouro, numero, complemento,\
			bairro, cidade, uf, pk,))
			conn.commit()
			conn.close()
			redirect('/index')
		except sqlite3.Error as erro:
			return "<script>alert('Não foi possível alterar o contato, ocorreu"\
			"o seguinte erro: ",erro.args[0],"')</script>",\
			"<script>window.history.back()</script>"
	
@route('/contato/exclui_contato/<pk:int>')
def exclui_contato(pk):
	try:
		conn = sqlite3.connect(banco)
		cursor = conn.cursor()
		cursor.execute('''DELETE FROM agenda WHERE id=?''',(pk,))
		conn.commit()
		conn.close()
		redirect('/index')
	except sqlite3.Error as erro:
		return "<script>alert('Não foi possível excluir, ocorreu o seguinte "\
		"erro: ",erro.args[0],"')</script>",\
		"<script>window.history.back()</script>"

@route('/static/<filename:path>')
def server_static(filename):
	return static_file(filename, root='static/')
	
@error(404)
def error404(error):
	return "Ops, página não encontrada!"


run(reloader=False, debug=False)