import mysql.connector 
import requests
import json
import webbrowser
import urllib.request
from bs4 import BeautifulSoup
import sys

class OpenFoodFactsReq:

    def __init__(self):
        #Initiate the connection to the base
        self.conn = mysql.connector.connect(host="localhost",user="root",password="felati61", database="test2")
        self.cursor = self.conn.cursor()

    def add_category(self,how_many):
        #get category on the categories page in json format
        api_url_fr = "https://fr.openfoodfacts.org/categories.json"
        api_url_en = "https://fr-en.openfoodfacts.org/categories.json"
        self.how_many = how_many
        i = 0
        request_data_fr = requests.get(api_url_fr)
        response_data_fr = request_data_fr.json()
        request_data_en = requests.get(api_url_en)
        response_data_en = request_data_en.json()

        while i<how_many:
            #Insert categories into the database
            add_data = ("INSERT IGNORE INTO categories (name_fr, name_en) VALUES (%s,%s)")
            self.cursor.execute(add_data,(response_data_fr['tags'][i]['name'],response_data_en['tags'][i]['name'],))
            self.conn.commit()
            i = i+1

    def add_food(self, nb_category, nb_food_per_category):
        #This function search and register the products per category
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
            id_3 = 1
            id_3_3 = str(id_3)
            id_2 = 1
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

                    try:
                        #Check if the indexes and keys are correct
                        product_barcode_done['product']['nutriments']['fat_value']
                        product_barcode_done['product']['nutriments']['salt_value']
                        product_barcode_done['product']['nutriments']['sugars']

                        #Conditions for a product and add it to the database
                        if len(product_barcode_done['product']['categories_tags']) > 5 and category_done['products'][id_3]['product_name'] != "" and product_barcode_done['product']['nutrition_grades_tags'][0] != "" and product_barcode_done['product']['nutrition_grades_tags'][0] != "unknown" and product_barcode_done['product']['nutrition_grades_tags'][0] != "not-applicable":

                            adding_food = ("INSERT IGNORE INTO food (name, categories4, categories_main, nutrition_score, fat_value, salt_value, sugars, barcode, brands) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                            self.cursor.execute(adding_food,(category_done['products'][id_3]['product_name'], product_barcode_done['product']['categories_tags'][5], category_saved, product_barcode_done['product']['nutrition_grades_tags'][0], product_barcode_done['product']['nutriments']['fat_value'], product_barcode_done['product']['nutriments']['salt_value'], product_barcode_done['product']['nutriments']['sugars'], category_done['products'][id_3]['codes_tags'][1], product_barcode_done['product']['brands']))
                            self.conn.commit()

                            id_2 = id_2 + 1
                            id_3 = id_3 + 1
                        #We know there is 20 products per page. So at 20 products, we go for the next page
                        elif len(category_done['products'])>=20:
                            page_id = page_id + 1
                            id_3 = 1
                            page_id_1 = str(page_id)

                        elif len(product_barcode_done['product']['categories_tags']) < 5:

                            id_3 = id_3 + 1
                    except (KeyError,IndexError):
                        id_3 = id_3 + 1
                #When all the products of the category are in database, we go for the next category.
                if id_2 == nb_food_per_category:       
                    id_i = id_i + 1
                    page_id = 1            
                    loop2 = 0
                    loop3 = 1


    def add_healthy_food(self, nb_categories_2, nb_products):
        #Here, we add healthy food compare to the product in database
        self.nb_categories_2 = nb_categories_2
        self.nb_products = nb_products
        test_1 = 1
        test_1_str = str(test_1)
        page_test = 1
        page_test_str = str(page_test)
        test_2 = 1
        test_2_str = str(test_2)
        produit_compteur = 1


        while test_2 < ((nb_products-1)*(nb_categories_2-1))+1:

            request_healthy = ("SELECT categories4 FROM food WHERE id = "+test_2_str+"")
            self.cursor.execute(request_healthy)
            request_healthy_done = str(self.cursor.fetchone()[0])

            request_healthy_3 = ("SELECT name FROM food WHERE id = "+test_2_str+"")
            self.cursor.execute(request_healthy_3)
            request_healthy_done_3 = str(self.cursor.fetchone()[0])

            request_healthy_4 = ("SELECT fat_value FROM food WHERE id = "+test_2_str+"")
            self.cursor.execute(request_healthy_4)
            request_healthy_done_4 = float(self.cursor.fetchone()[0])

            request_healthy_5 = ("SELECT sugars FROM food WHERE id = "+test_2_str+"")
            self.cursor.execute(request_healthy_5)
            request_healthy_done_5 = float(self.cursor.fetchone()[0])

            request_healthy_6 = ("SELECT salt_value FROM food WHERE id = "+test_2_str+"")
            self.cursor.execute(request_healthy_6)
            request_healthy_done_6 = float(self.cursor.fetchone()[0])


            if request_healthy_done.startswith('en:'):

                try:
                    #if the category is in english, we convert it into french to find the category page. I use beautiful soup to find meta data in the html page
                    pre_api_category_healthy = "https://fr.openfoodfacts.org/categorie/"+request_healthy_done+".json"
                    content = urllib.request.urlopen(pre_api_category_healthy).read()

                    soup = BeautifulSoup(content,"html.parser")
                    soup.prettify()
                    test_variable = soup.find("meta",  property="og:url")['content']

                    test_variable = soup.find("meta",  property="og:url")['content']
                    test_variable_fr = ""+test_variable+".json"


                    request_category_healthy = requests.get(test_variable_fr)
                    category_done_healthy = request_category_healthy.json()

                except TypeError:
                    produit_compteur = produit_compteur + 1

            else:
                #If the category is in french, we load it immediately into json
                pre_api_category_healthy = "https://fr.openfoodfacts.org/categorie/"+request_healthy_done+".json"
                request_category_healthy = requests.get(pre_api_category_healthy)
                category_done_healthy = request_category_healthy.json()

            #We check if we find product. If we don't find product, we add no substitute.
            if produit_compteur == len(category_done_healthy['products']) or produit_compteur == 19:
                print("Pas de correspondance trouvée")
                inserting_no_match = ("INSERT IGNORE INTO healthy_food (no_match) VALUES (%s)")
                self.cursor.execute(inserting_no_match, ("Pas de correspondance trouvée",))
                self.conn.commit()
                test_2 = test_2 + 1
                test_2_str = str(test_2)

                produit_compteur = 1

            try:
                category_done_healthy['products'][produit_compteur]['nutriments']['fat_value']
                category_done_healthy['products'][produit_compteur]['nutriments']['sugars']

                #We check if the subistute have less fat or sugar
                if request_healthy_done_3 != category_done_healthy['products'][produit_compteur]['product_name'] and float(category_done_healthy['products'][produit_compteur]['nutriments']['fat_value']) < request_healthy_done_4 or float(category_done_healthy['products'][produit_compteur]['nutriments']['sugars']) < request_healthy_done_5 or float(category_done_healthy['products'][produit_compteur]['nutriments']['salt_value']) < request_healthy_done_6:

                    get_healthy_food = ("INSERT IGNORE INTO healthy_food (name, categorie, barcode, fat_value, salt_value, sugars, brands) VALUES (%s,%s,%s,%s,%s,%s,%s)")
                    self.cursor.execute(get_healthy_food,(category_done_healthy['products'][produit_compteur]['product_name'], request_healthy_done, category_done_healthy['products'][produit_compteur]['codes_tags'][1], category_done_healthy['products'][produit_compteur]['nutriments']['fat_value'], category_done_healthy['products'][produit_compteur]['nutriments']['salt_value'], category_done_healthy['products'][produit_compteur]['nutriments']['sugars'], category_done_healthy['products'][produit_compteur]['brands'],))
                    self.conn.commit()
                    print("On vient d'ajouter un produit à la base !")

                    test_2 = test_2 + 1
                    test_2_str = str(test_2)

                    produit_compteur = 1

                else:
                    produit_compteur = produit_compteur + 1

            except (KeyError,IndexError):
                produit_compteur = produit_compteur + 1
            #When it's finish, we quit the loop
            if test_2 == nb_products*nb_categories_2:
                print("Tout les items sont entrés dans la base")
                test_1 = test_1 + 1
                test_2 = 1
                page_test = 1





        








            









