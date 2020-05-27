# https://benalexkeen.com/interacting-with-the-twitter-api-using-python/
import json
import math
import requests
import time
from datetime import datetime, timedelta


def premium_search(query, from_date, to_date, max_req, tweets_per_req, product, label, base_url, access_token):
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    retrieval_dates = generate_retrieval_dates(to_date, from_date, max_req)

    for key_date in retrieval_dates.keys():

        from_date_str = (key_date - timedelta(days=1)).strftime('%Y%m%d') + '0000'
        to_date_str = key_date.strftime('%Y%m%d') + '0000'

        search_params = {
            'query': query,
            'fromDate': from_date_str,
            'toDate': to_date_str,
            'maxResults': tweets_per_req
        }

        next_token = None

        for i in range(retrieval_dates[key_date]):

            if next_token:
                search_params['next'] = next_token

            search_url = '{}1.1/tweets/search/{}/{}.json'.format(base_url, product, label)
            search_resp = requests.get(search_url, headers=search_headers, params=search_params)
            result_data = search_resp.json()

            # used for testing
            # with open('test.json') as json_file:
            #     result_data = json.load(json_file)

            # print(json.dumps(result_data, indent=4))

            if 'error' in result_data:
                print(result_data['error'])
                return

            if len(result_data['results']) <= 0:
                continue

            result_request_params = result_data['requestParameters']
            result_time_format = '%Y%m%d%H%M'

            query_name = query
            country_name_pos = query.find('country:')
            if country_name_pos >= 0:
                query_name = query[country_name_pos: country_name_pos + len('country:') + 2]

            filename = '{}_{}_{}_{}_{}'.format(
                'premium-api',
                query_name.replace(' ', '-'),
                datetime.strptime(result_request_params['fromDate'], result_time_format).strftime('%Y-%m-%d'),
                datetime.strptime(result_request_params['toDate'], result_time_format).strftime('%Y-%m-%d'),
                # for testing
                # datetime.strptime(from_date_str, result_time_format).strftime('%Y-%m-%d'),
                # datetime.strptime(to_date_str, result_time_format).strftime('%Y-%m-%d'),
                i)

            with open(filename + '.json', 'w+') as outfile:
                json.dump(result_data, outfile, indent=4)

            print('Saved: ' + filename)

            time.sleep(3)

            if 'next' in result_data:
                # print('Next: ' + result_data['next'])
                next_token = result_data['next']
            else:
                # goto next day
                break


def generate_retrieval_dates(to_date, from_date, max_req):
    return_dates = {}
    delta_days = (to_date - from_date).days
    day_req_ratio = max_req / delta_days

    step_size = delta_days / (delta_days * day_req_ratio)
    step_range = round(delta_days * day_req_ratio)
    step_total = 0

    for i in range(0, step_range):
        retrieval_date = to_date - timedelta(days=math.floor(step_total))
        step_total += step_size
        return_dates[retrieval_date] = max(math.floor(day_req_ratio), 1)
    return return_dates

