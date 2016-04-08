# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Author:      Elder Sanitá Trevisan
#
# Copyright(©) 2016 Elder Sanitá Trevisan
# Licence:     GPL
#------------------------------------------------------------------------------
import sqlite3
import os


BASEDIR = os.path.dirname(__file__)
BANCO = os.path.join(BASEDIR, 'agenda.db')

ERROS = {"UNIQUE constraint failed: agenda.nome":"Contato já existente!"}


def criar_banco():
	try:
		con = sqlite3.connect(BANCO)
		cursor = con.cursor()
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS agenda
			(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			nome TEXT NOT NULL,
			telefone INTEGER NOT NULL,
			logradouro TEXT,
			numero INTEGER,
			complemento TEXT,
			bairro TEXT,
			cidade TEXT,
			uf TEXT,
			UNIQUE (nome)
			)
			''')
		con.commit()
	except sqlite3.Error as err:
		print(str(err.args[0]))
	finally:
		con.close()
		
def ler_todos_contatos():
	try:
		con = sqlite3.connect(BANCO)
		cursor = con.cursor()
		cursor.execute('''SELECT * FROM agenda ORDER BY nome ASC''')
		result = cursor.fetchall()
	except sqlite3.Error as err:
		raise "Ocorreu o seguinte erro: '%s'"%(str(err.args[0]))
	finally:
		con.close()
		return result
		
def ler_contato(pk):
	try:
		con = sqlite3.connect(BANCO)
		cursor = con.cursor()
		cursor.execute('''SELECT * FROM agenda WHERE id=?''',(pk,))
		result = cursor.fetchall()
	except sqlite3.Error as err:
		raise "Ocorreu o seguinte erro: '%s'"%(str(err.args[0]))
	finally:
		con.close()
		return result
	

def inserir_contato(*args):
	mg = None
	try:
		con = sqlite3.connect(BANCO)
		cursor = con.cursor()
		cursor.execute('''INSERT INTO agenda
							VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
							''', (None, args[0], args[1], args[2], args[3],\
							args[4], args[5], args[6], args[7]))
		con.commit()
	except sqlite3.Error as err:
		for erro,msg in ERROS.items():
			if erro == str(err.args[0]):
				mg = msg
			else:
				mg = "Ocorreu o seguinte erro: '%s'"%(str(err.args[0]))
		con.rollback()
	finally:
		con.close()
		return mg
		
def editar_contato(*args):	
	mg = None
	try:
		con = sqlite3.connect(BANCO)
		cursor = con.cursor()
		cursor.execute('''UPDATE agenda SET nome=?, telefone=?,
			logradouro=?, numero=?, complemento=?, bairro=?, cidade=?, uf=?
			WHERE id=?''',(args[0], args[1], args[2], args[3], args[4],\
			args[5], args[6], args[7], args[8]))
		con.commit()
	except sqlite3.Error as err:
		for erro,msg in ERROS.items():
			if erro == str(err.args[0]):
				mg = msg
			else:
				mg = "Ocorreu o seguinte erro: '%s'"%(str(err.args[0]))
		con.rollback()
	finally:
		con.close()
		return mg

def excluir_contato(pk):
	try:
		con = sqlite3.connect(BANCO)
		cursor = con.cursor()
		cursor.execute('''DELETE FROM agenda WHERE id=?''',(pk,))
		con.commit()
		return "Contato excluído com sucesso!"
	except sqlite3.Error as err:
		con.rollback()
		return "Ocorreu o seguinte erro: '%s'"%(str(err.args[0]))
	finally:
		con.close()

cdb = criar_banco()