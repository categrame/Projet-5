import mysql.connector 
import requests
import json
import webbrowser
import sys

from list_product import *

print("Création des bases de données en cours .... Veuillez patienter....")

conn = mysql.connector.connect(host="localhost",user="root",password="felati61", database="test2")
cursor = conn.cursor()

#clear tables before creating it
cursor.execute("""
DROP TABLE categories;
""")

cursor.execute("""
DROP TABLE food;
""")

cursor.execute("""
DROP TABLE healthy_food;
""")

#creation of the table to store the data from Open Food Fact API
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id int(5) NOT NULL AUTO_INCREMENT,
    name varchar(50) DEFAULT NULL,
    PRIMARY KEY(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS food (
    id int(5) NOT NULL AUTO_INCREMENT,
    name varchar(150) DEFAULT NULL,
    categories varchar(50) DEFAULT NULL,
    categories_main varchar(50) DEFAULT NULL,
    PRIMARY KEY(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS healthy_food (
    id int(5) NOT NULL AUTO_INCREMENT,
    name varchar(150) DEFAULT NULL,
    categories varchar(50) DEFAULT NULL,
    link varchar(200) DEFAULT NULL,
    PRIMARY KEY(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS my_products (
    id int(5) NOT NULL AUTO_INCREMENT,
    name varchar(150) DEFAULT NULL,
    categories varchar(50) DEFAULT NULL,
    link varchar(200) DEFAULT NULL,
    PRIMARY KEY(id)
);
""")

#In this loop, we fill the table categories
i = 0
while i<10:
	add_category = ("INSERT INTO categories (name) VALUES (%s)")
	cursor.execute(add_category, (category_add_db[i],))
	conn.commit()
	i = i+1

#Here we interact with the Open Food Fact API

y = 0
while y < 5:
	def get_data_sub():
		#Here is the url the get the data of the json file from http. I used the barcode of the product to find information about it.
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+drinks[y]+".json"
		#We store the data in a variable
		request_data = requests.get(api_url)
		#We return this variable into a json file
		return request_data.json()
	#datta-one represent the json file from the previous function
	data_one = get_data_sub()
	add_drinks = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	#We access json data like from a list
	cursor.execute(add_drinks,(data_one['product']['product_name'],drinks_cat[y],category_add_db[0]))
	conn.commit()
	y = y+1
#This entire file is based on the same way to work

#This is an indicator for database creation
print("5%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_drinks[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_drinks2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_drinks[x]+""
	cursor.execute(add_drinks2,(data_two['product']['product_name'],drinks_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("10%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+sugar_snacks[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_sugar_snacks = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_sugar_snacks,(data_one['product']['product_name'],sugar_snacks_cat[y],category_add_db[1]))
	conn.commit()
	y = y+1

print("15%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_sugar_snacks[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_sugar_snacks_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_sugar_snacks[x]+""
	cursor.execute(add_sugar_snacks_2,(data_two['product']['product_name'],sugar_snacks_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("20%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+milk_products[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_milk_products = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_milk_products,(data_one['product']['product_name'],milk_products_cat[y],category_add_db[2]))
	conn.commit()
	y = y+1

print("25%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_milk_products[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_milk_products_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_milk_products[x]+""
	cursor.execute(add_milk_products_2,(data_two['product']['product_name'],milk_products_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("30%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+prepared_dishes[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_prepared_dishes = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_prepared_dishes,(data_one['product']['product_name'],prepared_dishes_cat[y],category_add_db[3]))
	conn.commit()
	y = y+1

print("35%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_prepared_dishes[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_prepared_dishes_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_sugar_snacks[x]+""
	cursor.execute(add_prepared_dishes_2,(data_two['product']['product_name'],prepared_dishes_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("40%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+meat[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_meat = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_meat,(data_one['product']['product_name'],meat_cat[y],category_add_db[4]))
	conn.commit()
	y = y+1

print("45%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_meat[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_meat_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_meat[x]+""
	cursor.execute(add_meat_2,(data_two['product']['product_name'],meat_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("50%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+spreads[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_spreads = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_spreads,(data_one['product']['product_name'],spreads_cat[y],category_add_db[5]))
	conn.commit()
	y = y+1

print("55%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_spreads[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_spreads_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_spreads[x]+""
	cursor.execute(add_spreads_2,(data_two['product']['product_name'],spreads_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("60%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+green_products[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_green_products = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_green_products,(data_one['product']['product_name'],green_products_cat[y],category_add_db[6]))
	conn.commit()
	y = y+1

print("65%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_green_products[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_green_products_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_green_products[x]+""
	cursor.execute(add_green_products_2,(data_two['product']['product_name'],green_products_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("70%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+cheese[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_cheese = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_cheese,(data_one['product']['product_name'],cheese_cat[y],category_add_db[7]))
	conn.commit()
	y = y+1

print("75%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_cheese[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_cheese_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_cheese[x]+""
	cursor.execute(add_cheese_2,(data_two['product']['product_name'],cheese_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("80%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+fruits_vegetables_products[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_fruits_vegetables_products = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_fruits_vegetables_products,(data_one['product']['product_name'],fruits_vegetables_products_cat[y],category_add_db[8]))
	conn.commit()
	y = y+1

print("85%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_fruits_vegetables_products[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_fruits_vegetables_products_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_fruits_vegetables_products[x]+""
	cursor.execute(add_fruits_vegetables_products_2,(data_two['product']['product_name'],fruits_vegetables_products_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("90%")

y = 0
while y < 5:
	def get_data_sub():
		api_url = "https://world.openfoodfacts.org/api/v0/product/"+salty_snacks[y]+".json"
		request_data = requests.get(api_url)
		return request_data.json()
	data_one = get_data_sub()
	add_salty_snacks = ("INSERT INTO food (name, categories, categories_main) VALUES (%s,%s,%s)")
	cursor.execute(add_salty_snacks,(data_one['product']['product_name'],salty_snacks_cat[y],category_add_db[9]))
	conn.commit()
	y = y+1

print("95%")

x = 0
while x < 5:
	def get_data_sub2():
		api_url2 = "https://world.openfoodfacts.org/api/v0/product/"+healthy_salty_snacks[x]+".json"
		request_data2 = requests.get(api_url2)
		return request_data2.json()
	data_two = get_data_sub2()
	add_salty_snacks_2 = ("INSERT INTO healthy_food (name, categories, link) VALUES (%s,%s,%s)")
	open_food_facts_page = "https://fr.openfoodfacts.org/produit/"+healthy_salty_snacks[x]+""
	cursor.execute(add_salty_snacks_2,(data_two['product']['product_name'],salty_snacks_cat[x],open_food_facts_page))
	conn.commit()
	x = x + 1

print("100%")

print("Base de donnée opérationnelle !")
cursor.close()
conn.close()