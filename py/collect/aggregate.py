import os
import csv
import json


def aggregate(dirs):
    with open('aggregated_result.csv', 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['tweet_id', 'tweet_text', 'created_at', 'place_name', 'country', 'country_code'])
        for dir_path in dirs:
            write_csv_content_for_dir(writer, dir_path)


def write_csv_content_for_dir(csv_writer, dir_path):
    for json_filename in os.listdir(dir_path):
        if json_filename.endswith('.json'):
            with open('{}/{}'.format(dir_path, json_filename), 'r') as json_file:
                json_dic = json.load(json_file)
                for result in json_dic['results']:
                    tweet_id = result['id']
                    if result['truncated']:
                        tweet_text = '\"{}\"'.format(result['extended_tweet']['full_text'])
                    else:
                        tweet_text = '\"{}\"'.format(result['text'])
                    tweet_created_at = result['created_at']
                    if result['place']:
                        tweet_place_name = result['place']['name']
                        tweet_place_country = result['place']['country']
                        tweet_place_country_code = result['place']['country_code']
                    # elif result['retweeted_status']['place']:
                    #     tweet_place_name = result['retweeted_status']['place']['name']
                    #     tweet_place_country = result['retweeted_status']['place']['country']
                    #     tweet_place_country_code = result['retweeted_status']['place']['country_code']
                    # elif result['quoted_status']['place']:
                    #     tweet_place_name = result['quoted_status']['place']['name']
                    #     tweet_place_country = result['quoted_status']['place']['country']
                    #     tweet_place_country_code = result['quoted_status']['place']['country_code']
                    else:
                        continue
                    print('Added line: {},{},{},{},{},{}'.format(
                        tweet_id,
                        tweet_text,
                        tweet_created_at,
                        tweet_place_name,
                        tweet_place_country,
                        tweet_place_country_code))
                    csv_writer.writerow(
                        [tweet_id,
                         tweet_text,
                         tweet_created_at,
                         tweet_place_name,
                         tweet_place_country,
                         tweet_place_country_code])
