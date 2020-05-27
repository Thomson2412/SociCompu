# https://benalexkeen.com/interacting-with-the-twitter-api-using-python/
import json
import requests
import urllib.parse
from datetime import datetime


def standard_search(query, max_req, tweets_per_req, base_url, access_token):
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    next_token = None
    loop_count = 0

    while loop_count < max_req:

        search_params = {
            'q': query,
            'result_type': 'recent',
            'count': tweets_per_req
        }

        if next_token:
            search_params['max_id'] = next_token

        search_url = '{}1.1/search/tweets.json'.format(base_url)

        search_resp = requests.get(search_url, headers=search_headers, params=search_params)

        result_data = search_resp.json()
        print(json.dumps(result_data, indent=4))

        if 'error' in result_data:
            print(result_data['error'])
            break

        if len(result_data['statuses']) <= 0:
            break

        filename = '{}_{}_{}'.format(
            'standard-api',
            datetime.now().strftime('%Y-%m-%d'),
            loop_count)

        with open(filename + '.json', 'w+') as outfile:
            json.dump(result_data, outfile, indent=4)

        if 'next_results' in result_data['search_metadata']:
            query_string = result_data['search_metadata']['next_results'][1:]
            query_dic = urllib.parse.parse_qs(query_string)
            next_token = query_dic['max_id'][0]
        else:
            break

        loop_count += 1
