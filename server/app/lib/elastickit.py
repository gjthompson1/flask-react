import sys
sys.path.append('../..')

from elasticsearch import Elasticsearch

import csv
import time
import os

ELASTICSEARCH_HOST = 'elastic:changeme@docker.for.mac.localhost:9200'
print(ELASTICSEARCH_HOST, file=sys.stderr)
es = Elasticsearch([ELASTICSEARCH_HOST])

index_name = 'movie_index'
type_name = 'movie_doc'

def get_job_count():
    res = es.indices.stats(index_name, metric='docs')
    count = res['_all']['total']['docs']['count']
    results = {}
    results['count'] = count
    return results

def clean_hits(hits):
    out = []
    # print(hits, file=sys.stderr)
    for hit in hits:
        row = {}
        row['id'] = hit['_id']
        row['score'] = hit['_score']

        row['imdb_id'] = hit['_source'].get('imdb_id')
        row['title'] = hit['_source'].get('title')
        row['genres'] = hit['_source'].get('genres')
        row['overview'] = hit['_source'].get('overview')
        row['status'] = hit['_source'].get('status')
        row['spoken_languages'] = hit['_source'].get('release_date')
        row['release_date'] = hit['_source'].get('release_date')

        row['vote_average'] = hit['_source'].get('vote_average')
        row['vote_count'] = hit['_source'].get('vote_count')
        row['revenue'] = hit['_source'].get('revenue')
        row['runtime'] = hit['_source'].get('runtime')
        row['budget'] = hit['_source'].get('budget')
        row['popularity'] = hit['_source'].get('popularity')
        row['release_year'] = hit['_source'].get('release_year')
        row['spoken_languages_number'] = hit['_source'].get('spoken_languages_number')
        row['production_countries_number'] = hit['_source'].get('production_countries_number')

        row['original_language'] = hit['_source'].get('original_language')
        row['original_title'] = hit['_source'].get('original_title')
        row['production_companies'] = hit['_source'].get('production_companies')
        row['tagline'] = hit['_source'].get('tagline')

        row['scaled_vote_average'] = hit['_source'].get('scaled_vote_average')
        row['scaled_vote_count'] = hit['_source'].get('scaled_vote_count')
        row['scaled_revenue'] = hit['_source'].get('scaled_revenue')
        row['scaled_runtime'] = hit['_source'].get('scaled_runtime')
        row['scaled_budget'] = hit['_source'].get('scaled_budget')
        row['scaled_popularity'] = hit['_source'].get('scaled_popularity')
        row['scaled_release_year'] = hit['_source'].get('scaled_release_year')
        # row['spoken_languages_number'] = hit['_source'].get('spoken_languages_number')
        # row['production_countries_number'] = hit['_source'].get('production_countries_number')

        out.append(row)
    return out

def basic_search(query, search_filters, search_from, filter_ids):
    '''
        search_from=0
        search_filters=[
            {'field': 'country.keyword', 'value': 'United States'}
        ]
    '''

    should_terms = [
        {
            "multi_match": {
                "query": "{}".format(query),
                "fields": ['title','genres'],
            }
        }
    ]

    search_filters_clean = [{'term':{x['field']:x['value']}} for x in search_filters]

    if search_filters_clean == []:
        must_terms = [{"bool": {"should": should_terms}}]
    else:
        must_terms = search_filters_clean + [{"bool": {"should": should_terms}}]

    bdy = {
        "from" : search_from,
        "size" : 10,
        "query": {
            "bool": {
                "must": must_terms,
                "must_not": [{
                    'ids': {
                        'values':filter_ids
                    }
                }]
            }
        }
        # "aggs" : {
        #     "country" : {
        #         "terms" : {
        #             "field" : "country.keyword" ,
        #             "size": agg_counts.get('country',{}).get('count',5)
        #         }
        #     }
        # }
    }

    ans = es.search(index=index_name, doc_type=type_name ,body=bdy, size=10)
    # print(ans, file=sys.stderr)
    hits = ans.get('hits',{}).get('hits',{})

    took = ans.get('took','')
    results = {}
    results['took'] = took
    results['results'] = clean_hits(hits)
    results['num_results'] = ans.get('hits',{}).get('total','')
    # results['aggs'] = ans.get('aggregations',{})
    return results

def function_query(query, search_filters, search_from, logit_params, _type, filter_ids):
    '''
        search_from=0
        search_filters=[
            {'field': 'country.keyword', 'value': 'United States'}
        ]
    '''

    should_terms = [
        {
            "multi_match": {
                "query": "{}".format(query),
                "fields": ['title','genres','overview'],
            }
        }
    ]

    search_filters_clean = [{'term':{x['field']:x['value']}} for x in search_filters]

    if search_filters_clean == []:
        must_terms = [{"bool": {"should": should_terms}}]
    else:
        must_terms = search_filters_clean + [{"bool": {"should": should_terms}}]

    bdy = {
        "from" : search_from,
        "size" : 10,
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must_not": [{
                            'ids': {
                                'values':filter_ids
                            }
                        }]
                    }
                },
                "script_score": {
                    "script": {
                    "lang": "expression",
                    "source": '''
                        {}1/(1+ exp(-(
                            intercept +
                            doc['vote_average'].value * vote_average +
                            doc['vote_count'].value * vote_count +
                            doc['release_year'].value * release_year
                        )))
                    '''.format('-' if _type == 'worst' else '+'),
                    "params": {
                        "intercept": logit_params.get('intercept'),
                        "vote_average": logit_params.get('coef',{}).get('vote_average'),
                        "vote_count": logit_params.get('coef',{}).get('vote_count'),
                        "scaled_revenue": logit_params.get('coef',{}).get('scaled_revenue'),
                        "scaled_runtime": logit_params.get('coef',{}).get('scaled_runtime'),
                        "scaled_budget": logit_params.get('coef',{}).get('scaled_budget'),
                        "scaled_popularity": logit_params.get('coef',{}).get('scaled_popularity'),
                        "release_year": logit_params.get('coef',{}).get('release_year'),
                    }
                    # "source": "doc['release_year'].value"
                  }
                }
            }
        }
    }

    # _score/10 + 1/(1+ exp(-(doc['release_year'].value*a)))

    ans = es.search(index=index_name, doc_type=type_name ,body=bdy, size=10)
    # print(ans, file=sys.stderr)
    hits = ans.get('hits',{}).get('hits',{})

    took = ans.get('took','')
    results = {}
    results['took'] = took
    results['results'] = clean_hits(hits)
    results['num_results'] = ans.get('hits',{}).get('total','')
    # results['aggs'] = ans.get('aggregations',{})
    return results


                            # doc['scaled_vote_count'].value * scaled_vote_count +
                            # doc['scaled_revenue'].value * scaled_revenue +
                            # doc['scaled_runtime'].value * scaled_runtime +
                            # doc['scaled_budget'].value * scaled_budget +
                            # doc['scaled_popularity'].value * scaled_popularity +

    # _score/10000 +
    # bdy = {
    #     "from" : search_from,
    #     "size" : 10,
    #     "query": {
    #         "function_score": {
    #             "query": {
    #                 "bool": {
    #                     "must": must_terms
    #                 }
    #             },
    #             "script_score": {
    #                 "script": {
    #                 "lang": "expression",
    #                 "source": '''
    #                     1/(1+ exp(-(
    #                         intercept +
    #                         doc['scaled_vote_average'].value * scaled_vote_average +
    #                         doc['scaled_vote_count'].value*scaled_vote_count +
    #                         doc['scaled_revenue'].value*scaled_revenue +
    #                         doc['scaled_runtime'].value*scaled_runtime +
    #                         doc['scaled_budget'].value*scaled_budget +
    #                         doc['scaled_popularity'].value*scaled_popularity +
    #                         doc['scaled_release_year'].value*scaled_release_year
    #                     )))
    #                 ''',
    #                 "params": {
    #                     "intercept": logit_params.get('intercept'),
    #                     "scaled_vote_average": logit_params.get('coef',{}).get('scaled_vote_average'),
    #                     "scaled_vote_count": logit_params.get('coef',{}).get('scaled_vote_count'),
    #                     "scaled_revenue": logit_params.get('coef',{}).get('scaled_revenue'),
    #                     "scaled_runtime": logit_params.get('coef',{}).get('scaled_runtime'),
    #                     "scaled_budget": logit_params.get('coef',{}).get('scaled_budget'),
    #                     "scaled_popularity": logit_params.get('coef',{}).get('scaled_popularity'),
    #                     "scaled_release_year": logit_params.get('coef',{}).get('scaled_release_year'),
    #                 }
    #                 # "source": "doc['release_year'].value"
    #               }
    #             }
    #         }
    #     }
    # }
