import mysql.connector 
import requests
import json

#Here i stored all barcode and categories of products

category_add_db = ["Boissons", "Snacks sucrés", "Produits laitiers", "Plats préparés", "Viandes",
"Produits à tartiner", "Aliments d\'origine végétale", "Fromages", "Aliments à base de fruits et légumes", "Snacks salés"]

item_one = ["drinks", "sugar_snacks", "milk_products", "prepared_dishes", "meat", "spreads", "green_products", "cheese", "fruits_vegetables_products", "salty_snacks"]
item_two = ["healthy_drinks", "healthy_sugar_snacks", "healthy_milk_products", "healthy_prepared_dishes", "healthy_meat", "healthy_spreads", "healthy_green_products", "healthy_cheese", "healthy_fruits_vegetables_products", "healthy_salty_snacks"]
item_three = ["drinks_cat", "sugar_snacks_cat", "milk_products_cat", "prepared_dishes_cat", "meat_cat", "spreads_cat", "green_products_cat", "cheese_cat", "fruits_vegetables_products_cat", "salty_snacks_cat"]

drinks = ["8711000523544","5449000054227","7613035955783","3191010066302","3228886030011"]
healthy_drinks = ["3261342002108", "5449000052407", "3760091722577", "3092718605575", "3228886031421"]
drinks_cat = ["Café","Cola","Poudre chocolatée", "Sirop", "Thé Glacé"]

sugar_snacks = ["3350033279995", "7622210627087", "3770005306007", "3387390320008", "3178530407396"]
healthy_sugar_snacks = ["3596710451388", "4000539604201", "3760121212481", "8718885744019", "3229820786841"]
sugar_snacks_cat = ["Biscuits au chocolat", "Oeufs de Paques", "Chocolats Noir", "Barres de céréales", "Cookies"]

milk_products = ["3700311800562", "3248650204325", "3450970002318", "3033490215965", "3329778164064"]
healthy_milk_products = ["3451790887260", "20339906", "3661344795372", "3250392415846", "3760122960749"]
milk_products_cat = ["Crème fraiche", "Lait demi-ecrémé", "Flans", "Desserts au chocolat", "Yaourt à boire"]

prepared_dishes = ["3036811363567", "3596710439195", "3258561412443", "3350031937736", "20124571"]
healthy_prepared_dishes = ["3564700739815", "3083680484466", "3596710337729", "3000027364205", "3083681068344"]
prepared_dishes_cat = ["Soupes", "Taboulets", "Purée", "Pizzas", "Gratins"]

meat = ["3250392190729", "3266980467104", "3368954600569", "3258565412463", "3770009066020"]
healthy_meat = ["3250392493448", "2402735056488", "3256477039112", "3254565416838", "3770004620081"]
meat_cat = ["Porcs", "Dindes", "Escargots", "Boeufs", "Insectes"]

spreads = ["3760159101252", "3760109528092", "3442310000122", "3017620422003", "3144550006116"]
healthy_spreads = ["5400111093918", "3256225041886", "8712100876868", "3662072013370", "0022314030221"]
spreads_cat = ["Confitures de fraise", "Rillettes", "Beurres", "Pâtes à tartiner", "Crèmes de marron"]

green_products = ["3560070104413", "3770005467005", "3250390002123", "5200107657519", "8413762150203"]
healthy_green_products = ["3270160754731", "3270190128724", "3560070687619", "5200303003042", "3380390226400"]
green_products_cat = ["Champignons", "Farines", "Cacahouètes", "Huiles d'olive", "Graines de Tournesol"]

cheese = ["3250391257898", "26016986", "3660992001385", "5701638116631", "3272770097536"]
healthy_cheese = ["3294580948914", "3760099530334", "00672184", "3257980021199", "3480347290017"]
cheese_cat = ["Raclettes", "Fromages rapés", "Fromages à tartiner", "Fromages blanc", "Fromages Ail et fines herbes"]

fruits_vegetables_products = ["20645342", "3033610092124", "3263851481511", "3250391891832", "3162050018699"]
healthy_fruits_vegetables_products = ["5410188031072", "3245310024040", "3770001023779", "3760234880034", "3350030197643"]
fruits_vegetables_products_cat = ["Gazpacho", "Confts d'oignon", "Baies de Goji", "Mélanges de fruits secs", "Noix de coco"]

salty_snacks = ["20852924", "26038834", "3760181140182", "3577060101789", "3560070692842"]
healthy_salty_snacks = ["00498241", "3770001404042", "3270720001770", "3421557912092", "3483190000963"]
salty_snacks_cat = ["Chips au vinaigre", "Crackers", "Pistaches", "Pop corn salés", "Mini Saucissons secs"]
