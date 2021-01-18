import pymysql
import elasticsearch
from elasticsearch import helpers

conn = pymysql.connect(database='schoolshop', host='192.168.2.168', port=3306, user='root', password='199791')
cur = conn.cursor()
cur.execute('select name from school')
name_list = cur.fetchall()
es = elasticsearch.Elasticsearch(hosts='192.168.2.168')
actions = []
for name in name_list:
    action = {
        '_index': 'schoolshop',
        '_source': {
            'name': name[0],
            'nameSuggester': name[0]
        }
    }
    actions.append(action)
helpers.bulk(es, actions=actions)
