import sys
import requests
import base64
from datetime import datetime
from premium import premium_search
from standard import standard_search
from aggregate import aggregate


def main(arguments):
    if arguments[1] == 'standard' or arguments[1] == 'premium':
        query_base = 'air (quality OR pollution OR pollutants OR PM10 OR NO2 OR CO2 OR PM25) -is:retweet lang:en'

        base_url = 'https://api.twitter.com/'
        access_token = get_access_token(base_url, arguments[2], arguments[3])

        if arguments[1] == 'standard':
            search_standard_main(query_base, base_url, access_token)
        elif arguments[1] == 'premium':
            search_premium_main(query_base, base_url, access_token)

    elif arguments[1] == 'aggregate':
        # ['results_month', 'results_long/2020', 'results_long/2019']
        dir_paths = arguments[2].split(' ')
        aggregate_results(dir_paths)


def search_standard_main(query_base, base_url, access_token):
    standard_search(query_base, 5, 100, base_url, access_token)


def search_premium_main(query_base, base_url, access_token):
    product = 'fullarchive'
    label = 'devfa'

    from_date = datetime(2020, 3, 1)
    to_date = datetime(2020, 4, 30)

    premium_search(query_base + ' place_country:us', from_date, to_date, 8, 100, product, label, base_url, access_token)
    premium_search(query_base + ' place_country:gb', from_date, to_date, 8, 100, product, label, base_url, access_token)
    premium_search(query_base + ' place_country:in', from_date, to_date, 8, 100, product, label, base_url, access_token)

    from_date = datetime(2019, 3, 1)
    to_date = datetime(2019, 4, 30)

    premium_search(query_base + ' place_country:us', from_date, to_date, 8, 100, product, label, base_url, access_token)
    premium_search(query_base + ' place_country:gb', from_date, to_date, 8, 100, product, label, base_url, access_token)
    premium_search(query_base + ' place_country:in', from_date, to_date, 8, 100, product, label, base_url, access_token)


def aggregate_results(dir_paths):
    aggregate(dir_paths)


def get_access_token(base_url, key, secret):
    key_secret = '{}:{}'.format(key, secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    return auth_resp.json()['access_token']


if __name__ == "__main__":
    main(sys.argv)
