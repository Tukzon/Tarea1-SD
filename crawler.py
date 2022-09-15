# Imports para requests y parse de metadata
from keybert import KeyBERT
from bs4 import BeautifulSoup
from unicodedata import name
import requests

def parse_data(data_name, max_lines=None):
    with open(data_name, 'r', encoding="utf-8") as file:

        lines = file.readlines()[1:]

        # Para no exceder el límite propuesto
        count = 0

        for line in lines:
            if (count == max_lines):
                return

            parses = line.split('\t')

            # Evitamos las url en blanco. Es \n porque es el último término antes de un salto de linea.
            if (parses[4] == '\n'):
                continue

            url = parses[4]
            c_url = url[:-1]

            data = get_data_from_url(c_url)

            if data is not None:
                print(f'[{count}] {data["url"]}\n Title: {repr(data["title"])}\n Description: {repr(data["description"])}\n Keywords: {repr(data["keywords"])}')
                get_insert_query(data, count)
                count += 1

    return


def get_insert_query(data, id):
    print('getting query...')
    query = 'INSERT INTO data (id, url, title, description, keywords) VALUES ("%s", "%s", "%s", "%s", "%s");' % (
        id, data['url'], data['title'], data['description'], data['keywords'])
    with open('./db/init.sql', 'a', encoding="utf-8") as f:
        f.write(query + '\n')


def get_data_from_url(url):
    collected_data = {'url': url, 'title': None,'description': None, 'keywords': None}
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
                keywords = keywords['content'] if keywords else None
                keywords = keywords.replace(" ", "") if keywords else None
                keywords = keywords.replace(".", "") if keywords else None
                keywords = keywords.split(",") if keywords else None

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
    ht = parse_data(data_name, 5)
    
