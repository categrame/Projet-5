import mysql.connector 
import requests
import json
import webbrowser
import sys
import urllib.request
from bs4 import BeautifulSoup
from script_api_db_obj import *

name = OpenFoodFactsReq()

name.clear_db()

name.create_db()

name.add_category(5)

name.display_categories()

name.add_food(5,6)

name.add_healthy_food(5,6)


