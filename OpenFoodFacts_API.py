import mysql.connector 
import requests
import json
import webbrowser
import sys
import urllib.request
from bs4 import BeautifulSoup
from script_api_db_obj import *
from db_creation import *


#Variable to connect to MySQL database
host = "localhost"
user = "root"
password = "felati61"
database = "test2"

db_connect = DbConnect(host,user,password,database)

db_connect.clear_db()

db_connect.create_db()

APIReq = OpenFoodFactsReq()

APIReq.add_category(10)

APIReq.add_food(11,6)

APIReq.add_healthy_food(11,6)

conn = mysql.connector.connect(host=host,user=user,password=password, database=database)
cursor = conn.cursor()

loop_1 = 1

while loop_1:
	loop_2 = 0
	loop_1_1 = 0
	print("Bienvenue chez Pur Beurre, la start-up qui vous aide à mieux manger. Sélectionner une option dans le menu:")
	print("1 - Trouver un substitut d'un aliment")
	print("2 - Retrouver mes aliments substitués")
	#Here we wait for user answer
	user_choice_one = int(input())

	if user_choice_one == 1: #Acces in the first category if the user type "1"
		loop_2 = 1
		print("Dans quelle catégorie souhaitez-vous substituer un aliment ?")
	if user_choice_one == 2: #Acces in the second category if the user type "2"
		loop_1_1 = 1
	else:
		print("Vous n'avez pas saisi le nombre correct, veuillez recommencer !")

	while loop_1_1:
		#Here we display the food saved in a database
		print("Voici les aliments que vous avez sauvegardé:")
		display_saved_food = ("SELECT id, name, categories, link FROM my_products") #The SQL query
		cursor.execute(display_saved_food) #We execute the request
		row_saved = cursor.fetchall() #Organize the data
		for saved_row in row_saved: #For loop to print all data
			print(saved_row)
		print("Retourner au menu ? Tapez 1 pour oui et 2 pour quitter")
		try:
			quit_loop_1_1 = int(input())
			if quit_loop_1_1 == 1:
				loop_1_1 = 0
			elif quit_loop_1_1 == 2:
				quit()
				sys.exit()
		except:
			print("Je n'ai pas compris la réponse")
			


	while loop_2:
		#This the part of the program wich is permit to select and substitute food for something more healthy
		display_categories = ("SELECT id, name_fr FROM categories")
		cursor.execute(display_categories)
		rows = cursor.fetchall()
		for row in rows:
			print(row)
		print("Dans quelle catégorie voulez-vous chercher un substitut ? Entrez un nombre: ")
		answer_categories = str(input())
		#There is 10 categories. The user must choice between few categories
		category_choice = ("SELECT name_fr FROM categories WHERE id ="+answer_categories+"")
		cursor.execute(category_choice)
		rows2 = str(cursor.fetchone()[0])
		print("Vous avez choisi la catégorie :")
		print(rows2)

		#Its displays 5 products for the category. You must choose one to substitute it
		print("Voici les produits pour cette catégorie: ")
		category_display = ("SELECT id, name FROM food WHERE categories_main =(%s)")
		cursor.execute(category_display,(rows2,))
		rows5 = cursor.fetchall()
		for row5 in rows5:
			print(row5)
		loop_3 = 1

		while loop_3:
			#This loop is used replace the products and display it.
			print("Quel produit voulez-vous substituer ?")
			substitute_product = int(input())

			substitute_display = ("SELECT name FROM healthy_food WHERE id=%s")
			cursor.execute(substitute_display,(substitute_product,))
			rows7 = str(cursor.fetchone()[0])

			substitute_details = ("SELECT barcode FROM healthy_food WHERE id=%s")
			cursor.execute(substitute_details,(substitute_product,))
			rows8 = str(cursor.fetchone()[0])
			details_final = "https://fr.openfoodfacts.org/produit/"+rows8


			print("Nous vous proposons, ce produit : "+rows7)
			loop_3_1 = 1
			loop_3_1_1 = 0
			while loop_3_1:
				#Here you can register the product in the database. You can also open a link to the openfoodfact site.
				print("Voulez-vous accèder à la fiche de ce produit ? (Tapez 1 pour oui et 2 pour non")
				try:
					ask_page_product = int(input())
					if ask_page_product == 1:
						#here is the function to open the link in navigator
						webbrowser.open(details_final, new=2)
						loop_3_1_1 = 1
					elif ask_page_product == 2:
						loop_3_1_1 = 1
				except:
					print("Je n'ai pas compris la réponse veuillez recommencer.")


				while loop_3_1_1:

					print("Voulez-vous enregistrer ce produit dans votre base de donnée ? tapez 1 pour oui et 2 pour non")
					try:
						ask_register_bdd = int(input())

						if ask_register_bdd == 1:
							add_in_my_products = ("INSERT INTO my_products (name, link) VALUES (%s,%s)")
							cursor.execute(add_in_my_products,(rows7,details_final,))
							conn.commit()
							print("Le produit est bien enregistré dans la base.")
							#Here we asks the user to choose if she/he wants to choose another product to substitute, return to the main menu or leave the program
							print("Voulez-vous chercher un autre aliment à substituer ? Tapez 1 pour oui, 2 pour revenir au menu et 3 pour quitter le logiciel")
							try:
								ask_another_one = int(input())
								if ask_another_one == 1:
									loop_3_1_1 = 0
									loop_3_1 = 0
									loop_3 = 0
								elif ask_another_one == 2:
									loop_3_1_1 = 0
									loop_3_1 = 0
									loop_3 = 0
									loop_2 = 0
								elif ask_another_one == 3:
									sys.exit()
							except:
								print("Je n'ai pas compris la réponse veuillez recommencer")
						elif ask_register_bdd == 2:
							#Message in the case you didn't register the product in the database
							print("Vous n'avez pas enregistré le produit dans la base de donnée")
							print("Voulez-vous chercher un autre aliment à substituer ? Tapez 1 pour oui, 2 pour revenir au menu et 3 pour quitter le logiciel")
							try:
								ask_another_one = int(input())
								if ask_another_one == 1:
									loop_3_1_1 = 0
									loop_3_1 = 0
									loop_3 = 0
								elif ask_another_one == 2:
									loop_3_1_1 = 0
									loop_3_1 = 0
									loop_3 = 0
									loop_2 = 0
								elif ask_another_one == 3:
									quit()
									sys.exit()
							except:
								print("Je n'ai pas compris la réponse veuillez recommencer")
					except:
						print("Je n'ai pas compris la réponse veuillez recommencer")
#Close MySQL connection and loop
cursor.close()
conn.close()
if loop_1 == 1:
	quit()


