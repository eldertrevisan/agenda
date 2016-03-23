#-*- coding: utf-8 -*-
#Script para agilizar o processo de criação do banco de dados
import sqlite3

conn = sqlite3.connect('agenda.db')

cursor = conn.cursor()

cursor.execute('''
		CREATE TABLE IF NOT EXISTS agenda
		(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nome TEXT NOT NULL,
		telefone TEXT NOT NULL,
		logradouro TEXT,
		numero INTEGER,
		complemento TEXT,
		bairro TEXT,
		cidade TEXT,
		uf TEXT,
		UNIQUE (nome)
		)
		''')

conn.close()