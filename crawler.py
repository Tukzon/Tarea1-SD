# Imports para requests y parse de metadata
from ast import keyword
from keybert import KeyBERT
from bs4 import BeautifulSoup
from unicodedata import name
import requests

def parse_data(data_name, max_lines=None):
    with open(data_name, 'r') as file:

        lines = file.readlines()

        # Para no exceder el límite propuesto
        count = 0

        for line in lines:
            if (count == max_lines):
                return

            parses = line.split('\t')
            id = int(parses[0])
            url = parses[4]
            c_url = url[:-1]
            data = get_data_from_url(c_url)

            if data is not None:
                print(f'[{id}],{data["url"]}\n Title: {repr(data["title"])}\n Description: {repr(data["description"])}\n Keywords: {repr(data["keywords"])}')
                get_insert_query(data, id)
                count += 1

    return


def get_insert_query(data, id):
    print('getting query...')
    keysw = ""
    for kw in data['keywords']:
        if kw == data['keywords'][len(data['keywords'])-1]:
            keysw += '\''+kw+'\''
        else:
            keysw += '\''+kw+ "\',"
    query = f'INSERT INTO data (id,url,title,description,keywords) VALUES ({id},\'{data["url"]}\', \'{data["title"]}\', \'{data["description"]}\', ARRAY[{keysw}]);'
    print(query)
    with open('./db/insert.txt', 'a', encoding="utf-8") as f:
        f.write(query + '\n')
        id +=1


def get_data_from_url(url):
    collected_data = {'url': url, 'title': None,'description': None, 'keywords': []}
    try:
        r = requests.get(url, timeout=1)
    except Exception:
        return None

    if r.status_code == 200:
        source = requests.get(url).text
        # Se puede usar BeautifulSoap u otra librería que parsee la metadata de los docuementos HTML.
        soup = BeautifulSoup(source, 'html.parser')

        # Obtenemos la metadata
        meta = soup.find("meta")

        # Obtenemos el título
        title = soup.find("meta", {'name': "title"})

        description = soup.find("meta", {'name': "description"})

        keywords = soup.find("meta", {'name': "keywords"})

        try:
            if keywords is None:
                return None
            else:
                title = title['content'] if title else None
                description = description['content'] if description else None
                description = description.replace('\n', ' ') if description else None
                description = description.replace('\r', ' ') if description else None
                description = description.replace('\t', ' ') if description else None
                description = description.replace("'", '') if description else None
                keywords = keywords['content'] if keywords else None
                keywords = keywords.replace(" ", "") if keywords else None
                keywords = keywords.replace(".", "") if keywords else None
                keywords = keywords.split(",") if keywords else None
                keywords = keywords.replace("'", "") if keywords else None

        except Exception:
            return None
        collected_data['title'] = title
        collected_data['description'] = description
        collected_data['keywords'] = keywords
        if (collected_data['keywords'] is None):
            return None
        return collected_data

    return None


if __name__ == "__main__":
    data_name = './user-ct-test-collection-09.txt'
    ht = parse_data(data_name, 50)
    
