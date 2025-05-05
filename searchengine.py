import requests
import json

# Gets JSON data from Google search API and stores it in search result files, returns number of files
def Lessons_Autosearch():

    API_KEY = open('API_KEY.txt').read()
    SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID.txt').read()

    search_query = 'Book skiing lessons in Canada'

    url = 'https://www.googleapis.com/customsearch/v1'

    search_index = 1
    FileID = 1

    for i in range(0,10):

        params = {
            'q': search_query,
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'start': search_index
        }

        response = requests.get(url, params=params)
        response = response.json()
        with open('searchresults/searchresult' + str(FileID) + '.txt', 'w') as f:
            json.dump(response, f)
        
        search_index = search_index + 10
        FileID = FileID + 1

    return FileID



# Gets links from the JSON stored in searchresults folder and searches for keywords: lesson, book
# saves them to a set passed into function

def save_links(listoflinks, filename):

    with open(filename , 'r') as f:
        results = json.load(f)
    # print(results['items'][0])
    if 'items' in results:
        for i in range(0,10):
            if 'lesson' and 'book' in str(results['items'][i]):
                listoflinks.add(results['items'][i]['link'])


# Takes a set of links obtained through parsing action of save_links() and stores them
# in a links.txt file

def get_links(number_of_files):

    links = set()

    for i in range(1, number_of_files):
        save_links(links, 'searchresults/searchresult' + str(i) + '.txt')

    with open('links.txt', 'w') as f:
        for link in links:
            f.write(link + "\n")
    


    print(links)


if __name__ == "__main__":
    FileID = Lessons_Autosearch()
    get_links(FileID)