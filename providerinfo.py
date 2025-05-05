from parsing import get_base_url, parsing_with_gemininochunks
import getpass
import requests
import tldextract
import mysql.connector

extractor = tldextract.TLDExtract(suffix_list_urls=[], cache_dir=False)
count = 0

def get_domain(url):
    return extractor(url).domain



# Establishes connection using mysql connector with database

password = getpass.getpass('type password: ')
connection = mysql.connector.connect(
    user="slaiu-db",
    host="mysql-slaiu-db.alwaysdata.net",
    port="3306",
    password=password,
    database="slaiu-db_data")

cursor = connection.cursor()

API_KEY = open('API_KEY.txt').read()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID.txt').read()



# clears providerinfo table for new data to be added
def reset_table(name):
    cursor.execute(f"delete from {name};")
    cursor.execute(f"ALTER TABLE {name} AUTO_INCREMENT = 1;")

reset_table('providerinfo')

cursor.execute("SELECT link from lessons;") # gets all the links in the lessons table

bases = []

for link, in cursor:     
    link_base = get_base_url(link)
      
    if link_base not in bases:
        bases.append(link_base)
    
prompt = f'''Where is this provider of ski lessons location using the data provided.

Read the data carefully. Fill in any gaps in information using the internet and this link: {link_base}.

REMEMBER: Blue mountain is in Blue Mountains, Ontario, Canada
Provide your response like this: City, Province/State, Country

An example of a response could be: Banff, British Columbia, Canada

IMPORTANT: Only use this template for your response, do not provide any explanations or extra content

if you cannot find a location: Location Not Found in Database
'''

# Uses google search API to find location info of each lesson provider
for link_base in bases:

    domain = get_domain(link_base)

    search_query = "Where is " + domain + " located?"

    url = 'https://www.googleapis.com/customsearch/v1'

    search_index = 1

    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'start': search_index
    }

    response = requests.get(url, params=params)
    response = response.json()

    # the data returned is processed by Gemini for the relevant information which is directly inserted.
    try:
        # print(str(response["items"][0]))
        result = parsing_with_gemininochunks(str(response["items"]), prompt)
        # print(result)
        cursor.execute(f"INSERT INTO providerinfo (Link, provider_name, location) VALUES ('{link_base}', '{domain}', '{result}');")
        connection.commit()
        count = count + 1
    except Exception as problem:
        print(problem)
        continue


# This updates the lessons table with provider_id that corresponds to each lesson, this allows keybased relations in the database
for id in range(1, count + 1):
    cursor.execute(f"Select provider_name from providerinfo where ID = {id};")
    name = cursor.fetchone()[0]
    cursor.execute(f"Update lessons set provider_id = {id} where link like '%{name}%';")
    connection.commit()


