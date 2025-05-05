from bs4 import BeautifulSoup as bs
import requests
import json
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Takes links from a links.txt file and obtains the link base (eg: www.skilessons.com) and
# the robots.txt file link (eg: www.skilessons.com/robots.txt)

def get_robo_and_baselinks(robotlinks, baselinks):

    with open('links.txt', 'r') as file:
        for link in file:
            pattern = r"/"
            target = link
            wordsplit = re.split(pattern, target)
            RoLnk = wordsplit[0] + '//' + wordsplit[2] + '/robots.txt'
            BaseLnk = wordsplit[0] + '//' + wordsplit[2]
            baselinks.append(BaseLnk)
            robotlinks.append(RoLnk)



# Accepts as parameter a list of robots.txt links and checks each link for
# the lines (User-agent: *\nDisallow: /\n) which implies the website stakeholder owner does not want 
# any type of non human entity visiting the site. Otherwise, the base link is saved to a usable_links.txt file


def save_usablelinks(robotlinks_list):

    with open('links/usable_links.txt', 'w') as f:

        for i in range(0, len(robotlinks)):

            url = robotlinks[i]
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(1)
            page = driver.page_source
            driver.quit()
            soup = bs(page, 'html.parser')
            if ('User-agent: *\nDisallow: /\n' in soup.getText()):
                print('Noo')
            else:
                f.write(baselinks[i] + '\n') 

if __name__ == "__main__":
    robotlinks = []
    baselinks = []

    get_robo_and_baselinks(robotlinks, baselinks)
    print(robotlinks)

    save_usablelinks(robotlinks)





