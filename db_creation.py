import mysql.connector 
import requests
import json
import webbrowser
import urllib.request
from bs4 import BeautifulSoup
import sys

class DbConnect:

	def __init__(self,host,user,password,database):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.conn = mysql.connector.connect(host=host,user=user,password=password, database=database)
		self.cursor = self.conn.cursor()
		
	def clear_db(self):
		self.cursor.execute("""
		DROP TABLE categories, food, healthy_food;
		""")

	def create_db(self):
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS categories (
		id int(5) NOT NULL AUTO_INCREMENT,
		name_fr varchar(50) DEFAULT NULL,
		name_en varchar(50) DEFAULT NULL,
		PRIMARY KEY(id)
		);
		""")
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS my_products (
		id int(5) NOT NULL AUTO_INCREMENT,
		name varchar(250) DEFAULT NULL,
		categories varchar(50) DEFAULT NULL,
		link varchar(250) DEFAULT NULL,
		barcode varchar(250) DEFAULT NULL,
		PRIMARY KEY(id)
		);
		""")
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS healthy_food (
		id int(5) NOT NULL AUTO_INCREMENT,
		name varchar(250) DEFAULT NULL,
		categorie varchar(50) DEFAULT NULL,
		barcode varchar(20) DEFAULT NULL,
		fat_value float(5) DEFAULT NULL,
		salt_value float(5) DEFAULT NULL,
		sugars float(5) DEFAULT NULL,
		brands varchar(250) DEFAULT NULL,
		no_match varchar(50) DEFAULT NULL,
		PRIMARY KEY(id)
		);
		""")
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS food (
		id int(5) NOT NULL AUTO_INCREMENT,
		name varchar(250) DEFAULT NULL,
		categories4 varchar(100) DEFAULT NULL,
		categories_main varchar(50) DEFAULT NULL,
		nutrition_score varchar(2) DEFAULT NULL,
		fat_value float(5) DEFAULT NULL,
		salt_value float(5) DEFAULT NULL,
		sugars float(5) DEFAULT NULL,
		brands varchar(250) DEFAULT NULL,
		barcode varchar(20) DEFAULT NULL,
		link varchar(250) DEFAULT NULL,
		PRIMARY KEY(id)
		);
		""")
		return print("Bases crées avec succès")