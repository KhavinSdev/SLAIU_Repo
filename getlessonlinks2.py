from bs4 import BeautifulSoup
from scraping import (scrape_site, split_dom_content, getlinks)
from parsing import parsing_with_gemini, parsing_with_gemininochunks, appreciate, get_base_url
import time

import re

pattern1 = r"/"
pattern2 = r"."

# similar to getlessonlinks1.py
parse_description = """

You will examine a list of links provided. You will find the links which may take the user to a page where they can
book skiing lessons. If a is link provided. 

Look for keywords like: lessons, youth lessons, adult, family, group, clubs, camps, etc.
be liberal with how many links found that you consider.

You can format the output like this:

https://skilessonok.com/winter/snow-school/adults/
https://skilessonok.com/winter/snow-school/kids/
https://skilessonok.com/winter.snow-school/family

Only provide this output, no other extra explanation or text. Don't leave a new line at the end of your response.
If you cannot find any links relevant, simply output EMPTY

REMEMBER: Don't repeat the same link multiple times in your response.
"""


current_link_num = 1


links_saved = []    # keeps track of already saved links

# Gets links if already present in save file. Skip if any errors are present
try:
    with open('links/AIconsolidatelinks.txt', 'r') as f:
        contents = f.read()
        if contents:
            links_saved = [line.strip() for line in f]
        else:
            pass
except:
    pass

# Function accepts a previous link storage file (link1), a new one (link2) and a local links_saved list
# This is for preventing redundancy
def getlessonlinks(link1, link2, links_saved):

    with open('links/' + link1, 'r') as links:
        for link in links:
            link = link.removesuffix("\n")  # Removes new line characters from each link
            if link in links_saved: # Repeated links are skipped
                continue
            try:
                url = link
                # print(url + ' This is the base\n')
                base = get_base_url(url) # Refer to parsing.py
                links = getlinks(url, base) # Refer to scraping.py

               
                dom_chunks = split_dom_content(links) # Refer to scraping.py
                result = parsing_with_gemininochunks(dom_chunks, parse_description) # Refer to parsing.py 

                if result == 'EMPTY\n':
                    continue
                print(repr(result))
                result_links = result.split("\n") # splits Gemini API response by line and stores each link as a list element
                links_saved = links_saved + result_links # adds the parsed links to the links_saved list

                
                           
            except:
                continue

        links_saved = list(set(links_saved)) # removes all duplicates
        with open('links/' + link2, 'a') as f:
            for item in links_saved:
                f.write(str(item) + '\n') # saves the links to a getlessonlinks2.txt file
        



    appreciate("Thank you for doing such a great job")
    links_saved.clear() # clears the links_saved list


# getlessonlinks('usable_links.txt', 'AIconsolidatelinks1.txt')
# performs more processing by repeating the above process and saving to a new file
getlessonlinks('AIconsolidatelinks3.txt', 'AIconsolidatelinks.txt', links_saved)