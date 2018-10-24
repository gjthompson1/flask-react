import sys
sys.path.append('..')

import re
import pandas as pd

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from sklearn.preprocessing import StandardScaler

from lib.mlkit import MODEL_COLUMNS

ELASTICSEARCH_HOST = 'elastic:changeme@localhost:9200'
es = Elasticsearch([ELASTICSEARCH_HOST], verify_certs=True)
es.info()

index_name = 'movie_index'
type_name = 'movie_doc'

CHUNK_SIZE = 1000
MAX_CHUNK_BYTES = 10000000

def convert_strings(val):
    return None if str(val).strip() in ['nan','None',''] else val

def convert_numbers(val):
    if str(val) in ['nan','None','']:
        res = None
    else:
        try:
            res = float(str(val))
        except:
            res = None
    return res

def date_to_year(val):
    if re.search('(18|19|20)',str(val)) != None:
        res = str(val).split('/')[-1]
        if len(res)==4:
            return res
        else:
            return None
    else:
        return None

def clean_row(row):
    d = {
    'imdb_id': convert_strings(row.get('imdb_id')),
    'title': convert_strings(row.get('title')),
    'genres': convert_strings(row.get('genres')),
    'overview': convert_strings(row.get('overview')),
    'status': convert_strings(row.get('status')),
    'spoken_languages': convert_strings(row.get('spoken_languages')),
    'release_date': convert_strings(row.get('release_date')),

    'vote_average': convert_numbers(row.get('vote_average')),
    'vote_count': convert_numbers(row.get('vote_count')),
    'revenue': convert_numbers(row.get('revenue')),
    'runtime': convert_numbers(row.get('runtime')),
    'budget': convert_numbers(row.get('budget')),
    'popularity': convert_numbers(row.get('popularity')),
    'release_year': convert_numbers(date_to_year(row.get('release_date'))),
    'spoken_languages_number': convert_numbers(row.get('spoken_languages_number')),
    'production_countries_number': convert_numbers(row.get('production_countries_number')),

    'original_language': convert_strings(row.get('original_language')),
    'original_title': convert_strings(row.get('original_title')),
    'production_companies': convert_strings(row.get('production_companies')),
    'tagline': convert_strings(row.get('tagline')),
    }
    return d


def _build_index_structure(index_name, type_name, row, _id):
    d = {
        '_index': index_name,
        '_type': type_name,
        '_id': str(_id),
        '_source': row
    }
    return d

def _robust_index(es, data):

    COMPLETE = 0
    actions = []
    x = 1
    for row in data:
        action = _build_index_structure(index_name, type_name, row, x)
        actions.append(action)
        x+=1

        if len(actions)>=CHUNK_SIZE:
            print("PUSHING TO ELASTICSEARCH, COMPLETE",COMPLETE)
            helpers.bulk(es, actions,request_timeout=60)
            COMPLETE+=len(actions)
            actions = []

    print("PUSHING TO ELASTICSEARCH, COMPLETE",COMPLETE)
    helpers.bulk(es, actions,request_timeout=60)
    COMPLETE+=len(actions)
    actions = []

## START INDEX ##

df = pd.read_csv('data/AllMoviesDetailsCleaned.csv',delimiter=';')
data = df.to_dict('records')
data = [clean_row(x) for x in data]

non_numeric = pd.DataFrame(data)
non_numeric = non_numeric[non_numeric.columns[~pd.Series(non_numeric.columns).isin(pd.Series(MODEL_COLUMNS))]]

to_scale = pd.DataFrame(data)[MODEL_COLUMNS]
to_scale = to_scale.apply(lambda x: x.fillna(x.median()),axis=0)

scaler = StandardScaler()
ans = scaler.fit_transform(to_scale)
scaled_df = pd.DataFrame(ans)
scaled_df.columns = ['scaled_{}'.format(x) for x in MODEL_COLUMNS]

# master = pd.concat([non_numeric, to_scale, scaled_df], axis=1)
# master = master.fillna('')
# master = master[master['vote_average'].apply(lambda x: x>0)]
# master = master[master['vote_count'].apply(lambda x: x>0)]
# master = master[master['revenue'].apply(lambda x: x>0)]
# master = master[master['runtime'].apply(lambda x: x>0)]
# master = master[master['budget'].apply(lambda x: x>0)]
# master = master[master['popularity'].apply(lambda x: x>0)]
# master = master[master['release_year'].apply(lambda x: x>0)]

master = master.to_dict('records')

_robust_index(es, master)
es.indices.put_settings(index=index_name,body= {"index" : {"max_result_window" : 5000}})

# es.indices.delete(index=index_name)

# types = []
# i = 0
# for row in data:
#     i+=1
#     print(i, end='\r')
#     if str(row['genres']) not in [None,'nan','']:
#         types = types + row['genres'].split('|')
#
# pd.Series(types).value_counts()
