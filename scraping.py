import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


# takes a link to a website as parameter and returns the raw html source
def scrape_site(site):
    print("Launching the browser(chrome)")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(site)
        print('Page loaded....')
        html = driver.page_source
        time.sleep(7)

        return html
    
    except:
        print("Website failed to load properly")


# Takes raw html and returns the body content as a string
def extract_body_content(htmlraw_data):
    soup = BeautifulSoup(htmlraw_data, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

# takes a url and its base and gets all the anchor (<a>) tages with the 'href'attribute and returns them as a list
def getlinks(url, base):
    contents = scrape_site(url)
    soup = BeautifulSoup(contents, "html.parser")
    soup = soup.find_all('a')
    links = []

    for i in soup:
        try:
            if(i['href'] == '#'):
                continue
            elif 'https' not in i:
                link = base + i['href']
                if link.count('http') > 1:
                    continue
                links.append(link)
            else:
                links.append(i['href'])

            
        except:
            continue

    links = '\n'.join(links)
    print(links)
    return links


# Removes any script or style tags from body and gets the innerHTML seperated on new lines and returns as a string
def clean_body_content(body_contents):
    soup = BeautifulSoup(body_contents, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

# takes long string (dom_content) and splits into chunks with a maximum length (max_length) and returns the chunks in a list 
def split_dom_content(dom_content, max_length = 10000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
