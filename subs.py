from bs4 import BeautifulSoup
import requests
import json

html_doc_deps = requests.get('https://matriculaweb.unb.br/graduacao/oferta_dep.aspx?cod=1').text

soup_deps = BeautifulSoup(html_doc_deps, 'html.parser')

table_deps = soup_deps.select('#datatable')[0] 
# import ipdb; ipdb.set_trace()
links_deps = table_deps.select('td > a')  
url_deps = [link['href']for link in links_deps]

all_subjects=[]
for url in url_deps[:10]:
    html_doc = requests.get(f'https://matriculaweb.unb.br/graduacao/{url}').text

    soup = BeautifulSoup(html_doc, 'html.parser')

    table = soup.select('#datatable')[0] 
    subjects_html = table.select('td > a')  
    subjects = [subject.text for subject in subjects_html]
    subjects = [ subject for subject in subjects if subject != 'event_note']

    all_subjects = all_subjects + subjects

data = {'subjects' : all_subjects}

with open('./subs.json', 'w') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False).encode('utf8')