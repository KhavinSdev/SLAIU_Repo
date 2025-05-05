from bs4 import BeautifulSoup
from scraping import (scrape_site, split_dom_content, clean_body_content, extract_body_content)
from parsing import parsing_with_gemini, parsing_with_gemininochunks, appreciate
import getpass
import mysql.connector
import time
import pandas as pd
import re

pattern1 = r"/"
pattern2 = r"."


# table for lesson details
table1 = 'lessons'
# table for lesson providers
table2 = 'providerinfo'

# Uses mysql connector to establish connection with database
password = getpass.getpass('type password: ')
connection = mysql.connector.connect(
    user="slaiu-db",
    host="mysql-slaiu-db.alwaysdata.net",
    port="3306",
    password=password,
    database="slaiu-db_data")

cursor = connection.cursor()

# deletes existing data from a table (name) for new records to be added
def reset_table(name):
    cursor.execute(f"delete from {name};")
    cursor.execute(f"ALTER TABLE {name} AUTO_INCREMENT = 1;")

reset_table(table1)
reset_table(table2)

# lessonproviders = [] # contains a list of lesson provider names

with open('links/AIconsolidatelinks.txt', 'r') as links:

    
        for link in links:
            # The prompt that is passed along with data to the Gemini API
            parse_description = f"""
You will be reviewing the data from a ski lessons booking website. If the site data indicates that the lesson is not about skiing, simply return EMPTY
else:

You will create a table from the data provided along with this prompt. The table should have the following columns: lesson, timing, dates, prices, age restrictions.
An example of a row in this table could be: ski lesson - private, 2, 2025/11/11 , 52, 12, family.
If you cannot find data for a specific column, please fill the cell with NULL.

Important: if the lesson, hours, and prices values you are inserting are null, then just output: EMPTY


You will then return the query to insert each record into an sql table called lessons, do not create the table.
the corresponding fields have the following datatypes:

lesson - varchar(255)
hours - int
prices - int
minimumage - int
lesson_type - varchar(20)
link - varchar(100)
available_from - date


Note: lesson_type can take only these values -> private, group, family.

follow the following template for your output:

INSERT INTO lessons (lesson, hours, prices, minimumage, lesson_type, link, available_from) VALUES ....

NOTE: link will always have the value {link}
Remember to use only a single insert statement.

Remember to end an sql query with a semicolon (;)

if the table you created was empty, simply output: EMPTY.
if multiple dates are present, insert the earliest date.

Only provide this output, no other extra explanation or text.

"""
            try:
                url = link

                # The following code scrapes the raw html data, processes and sends it to the Gemini API
                result = scrape_site(url)
                body_content = extract_body_content(result)
                cleaned_content = clean_body_content(body_content)
                
                dom_chunks = split_dom_content(cleaned_content)
                result = parsing_with_gemininochunks(dom_chunks, parse_description)

                # The data from the webpages is passed and Gemini structures the required information and returns the SQL queries to be executed.


                # print(result)

                # Only processes non empty results
                if result != 'EMPTY\n':
                    # print(link)
                    
                    # This section has been skipped in favour of a seperate handling python file and process for provider info
                    # THIS GETS THE PROVIDER NAME FROM THE LINK

                    # linkbase = re.split(pattern1, link)[2]
                    # linkbase = linkbase.split(pattern2)
                    # if linkbase[0] == 'www':
                    #     provider = linkbase[1]
                    # else:
                    #     provider = linkbase[0]
                    
                    # if provider not in lessonproviders: # adds the provider name to the lessonproviders list
                    #     lessonproviders.append(provider)
                        

                    cursor.execute(result)
                    connection.commit()
                    # print(cursor.rowcount)

                    with open('nonemptylinks.txt', 'a') as NonEmptyLinks: # helps identify non-empty links for future
                         NonEmptyLinks.write(url)

                continue


            except Exception as e:
                # print(e)
                continue
        
appreciate("Thank you for doing such a great job")
            
        

        

