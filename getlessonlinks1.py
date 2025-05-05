from bs4 import BeautifulSoup
from scraping import (scrape_site, split_dom_content, getlinks)
from parsing import parsing_with_gemini, parsing_with_gemininochunks, appreciate
import time

import re

# patterns for link formatting
pattern1 = r"/"
pattern2 = r"."

# prompt to be passed to Gemini API for parsing
parse_description = """

You will examine a list of links provided. You will find the links which may take the user to a page where they can
book skiing lessons,

You can format the output like this:

https://lessons-skifun.com/winter/snow-school/adults/
https://lessons-skifun.com/winter/snow-school/kids/
https://lessons-skifun.com/winter.snow-school/family

Only provide this output, no other extra explanation or text. Don't leave a new line at the end of your response.
If you cannot find any links relevant to the above context, simply output EMPTY

"""

# Takes each link from usable_links.txt and scrapes links from its associated page
# these links are passed to the Gemini API to judge their relevance and relevant links are saved

current_link_num = 1

with open('usable_links.txt', 'r') as links:
    for link in links:
        try:
            url = link
            # print(url + ' This is the base\n')
            
            # Refer to scraping.py for explanation
            links = getlinks(url)                                               
            dom_chunks = split_dom_content(links)

            # Refer to parsing.py for explanation                               
            result = parsing_with_gemininochunks(dom_chunks, parse_description) 

            print(result)

            # Empty results are ignored, else saved
            if result == 'EMPTY\n':
                continue
            else:
                with open('AIconsolidatelinks.txt', 'a') as f:
                    f.write(result)

        # There is a tendency for Errors due to formatting issues, it is simpler to ignore rather than handle at present.
        # This part of the project is not crucial to each user request so such work arounds are allowed     
        except:
            continue

appreciate("Thank you for doing such a great job")