import mysql.connector 
import requests
import json
import webbrowser
import urllib.request
from bs4 import BeautifulSoup
import sys

class OpenFoodFactsReq:

    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost",user="root",password="felati61", database="test2")
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
        CREATE TABLE IF NOT EXISTS healthy_food (
        id int(5) NOT NULL AUTO_INCREMENT,
        name varchar(50) DEFAULT NULL,
        categorie varchar(50) DEFAULT NULL,
        barcode varchar(20) DEFAULT NULL,
        no_match varchar(50) DEFAULT NULL,
        PRIMARY KEY(id)
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS food (
        id int(5) NOT NULL AUTO_INCREMENT,
        name varchar(150) DEFAULT NULL,
        categories1 varchar(50) DEFAULT NULL,
        categories2 varchar(50) DEFAULT NULL,
        categories3 varchar(50) DEFAULT NULL,
        categories4 varchar(100) DEFAULT NULL,
        categories_main varchar(50) DEFAULT NULL,
        nutrition_score varchar(2) DEFAULT NULL,
        barcode varchar(20) DEFAULT NULL,
        PRIMARY KEY(id)
        );
        """)

    def display_categories(self):
        display_something = ("SELECT name_fr, name_en FROM categories") #The SQL query
        self.cursor.execute(display_something) #We execute the request
        row_saved = self.cursor.fetchall() #Organize the data
        for saved_row in row_saved: #For loop to print all data
            print(saved_row)

    def add_category(self,how_many):
        api_url_fr = "https://fr.openfoodfacts.org/categories.json"
        api_url_en = "https://fr-en.openfoodfacts.org/categories.json"
        self.how_many = how_many
        i = 0
        request_data_fr = requests.get(api_url_fr)
        response_data_fr = request_data_fr.json()
        request_data_en = requests.get(api_url_en)
        response_data_en = request_data_en.json()

        while i<how_many:
            add_data = ("INSERT INTO categories (name_fr, name_en) VALUES (%s,%s)")
            self.cursor.execute(add_data,(response_data_fr['tags'][i]['name'],response_data_en['tags'][i]['name'],))
            self.conn.commit()
            i = i+1

    def add_food(self, nb_category, nb_food_per_category):
        self.nb_food_per_category = nb_food_per_category 
        self.nb_category = nb_category
        id_i = 1
        id_2 = 1
        id_healthy_food = 1
        page_id = 1


        while id_i < nb_category:

            id_1 = str(id_i)
            page_id_1 = str(page_id)
            choose_category = ("SELECT name_fr FROM categories WHERE id = "+id_1+"")

            self.cursor.execute(choose_category) #We execute the request
            category_saved = str(self.cursor.fetchone()[0]) #Organize the data

            print(category_saved)

            id_2 = 1
            id_3 = 1
            id_3_3 = str(id_3)
            id_4 = 1
            self.nb_category = nb_category
            lower = 1
            loop2 = 1
            loop3 = 0


            while loop2:

                while lower <= id_2 < nb_food_per_category:

                    api_category = "https://fr.openfoodfacts.org/categorie/"+category_saved+"/"+page_id_1+".json"
                    request_category = requests.get(api_category)
                    category_done = request_category.json()

                    test128 = str(category_done['products'][id_3]['codes_tags'][1])

                    api_product_barcode = "https://fr.openfoodfacts.org/api/v0/product/"+test128+".json"
                    request_product_barcode = requests.get(api_product_barcode)
                    product_barcode_done = request_product_barcode.json()

                    if len(product_barcode_done['product']['categories_tags']) > 3 and category_done['products'][id_3]['product_name'] != "" and product_barcode_done['product']['nutrition_grades_tags'][0] != "" and product_barcode_done['product']['nutrition_grades_tags'][0] != "unknown" and product_barcode_done['product']['nutrition_grades_tags'][0] != "not-applicable":

                        adding_food = ("INSERT INTO food (name, categories4, categories_main, nutrition_score, barcode) VALUES (%s,%s,%s,%s,%s)")
                        self.cursor.execute(adding_food,(category_done['products'][id_3]['product_name'], product_barcode_done['product']['categories_tags'][3], category_saved, product_barcode_done['product']['nutrition_grades_tags'][0], category_done['products'][id_3]['codes_tags'][1],))
                        self.conn.commit()

                        print(id_2)

                        id_2 = id_2 + 1
                        id_3 = id_3 + 1

                    elif len(category_done['products'])>=20:
                        page_id = page_id + 1
                        id_3 = 1
                        page_id_1 = str(page_id)

                    elif len(product_barcode_done['product']['categories_tags']) < 3:

                        id_3 = id_3 + 1

                if id_2 == nb_food_per_category:       
                    id_i = id_i + 1
                    page_id = 1            
                    loop2 = 0
                    loop3 = 1


    def add_healthy_food(self, nb_categories_2, nb_products):
        self.nb_categories_2 = nb_categories_2
        self.nb_products = nb_products
        test_1 = 1
        test_1_str = str(test_1)
        page_test = 1
        page_test_str = str(page_test)
        test_2 = 1
        test_2_str = str(test_2)
        produit_compteur = 1
        while test_1 < nb_categories_2:

            print("premier palier")

            loop_test = 1


            while loop_test:

                while test_2 < nb_products*nb_categories_2:
                    print("deuxieme palier")

                    no_match_oui = "Pas de produit"

                    request_healthy = ("SELECT categories4 FROM food WHERE id = "+test_2_str+"")
                    self.cursor.execute(request_healthy)
                    request_healthy_done = str(self.cursor.fetchone()[0])

                    request_healthy_3 = ("SELECT name FROM food WHERE id = "+test_2_str+"")
                    self.cursor.execute(request_healthy_3)
                    request_healthy_done_3 = str(self.cursor.fetchone()[0])

                    pre_api_category_healthy = "https://fr.openfoodfacts.org/categorie/"+request_healthy_done+".json"
                    content = urllib.request.urlopen(pre_api_category_healthy).read()

                    soup = BeautifulSoup(content,"html.parser")
                    soup.prettify()
                    test_variable = soup.find("meta",  property="og:url")['content']

                    test_variable = soup.find("meta",  property="og:url")['content']
                    test_variable_fr = ""+test_variable+".json"


                    request_category_healthy = requests.get(test_variable_fr)
                    category_done_healthy = request_category_healthy.json()

                    print(produit_compteur)
                    print(test_2_str)
                    #print(category_done_healthy['products'][produit_compteur]['categories_tags'][5])

                    if produit_compteur == len(category_done_healthy['products']):
                        print("Pas de correspondance trouvée")
                        test_2 = test_2 + 1
                        test_2_str = str(test_2)

                        produit_compteur = 1

                    if request_healthy_done_3 != category_done_healthy['products'][produit_compteur]['product_name']:

                        get_healthy_food = ("INSERT INTO healthy_food (name, categorie, barcode) VALUES (%s,%s,%s)")
                        self.cursor.execute(get_healthy_food,(category_done_healthy['products'][produit_compteur]['product_name'], request_healthy_done, category_done_healthy['products'][produit_compteur]['codes_tags'][1],))
                        self.conn.commit()
                        print("On vient d'ajouter un produit à la base !")

                        test_2 = test_2 + 1
                        test_2_str = str(test_2)

                    else:
                        produit_compteur = produit_compteur + 1

                if test_2 == nb_products:
                    print("Quand tout est accomplit on sort de la page")
                    test_1 = test_1 + 1
                    page_test = 1
                    loop_test = 0





        








            








