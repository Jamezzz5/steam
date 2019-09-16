import os
import sys
import json
import time
import random
import logging
import argparse
import requests
import pandas as pd
import datetime as dt


def set_log():
    formatter = logging.Formatter('%(asctime)s [%(module)14s]'
                                  '[%(levelname)8s] %(message)s')
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    log.addHandler(console)

    try:
        log_file = logging.FileHandler('logfile.log', mode='w')
        log_file.setFormatter(formatter)
        log.addHandler(log_file)
    except PermissionError as e:
        logging.warning('Could not open logfile with error: \n {}'.format(e))


parser = argparse.ArgumentParser()
parser.add_argument('--loop', metavar='N', type=int)
args = parser.parse_args()


class SteamApi(object):
    first_steam_id = 76561197960265729
    total_steam_users = (10 ** 9) * 4
    last_steam_id = first_steam_id + total_steam_users
    default_search_num = 10 ** 5
    base_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'

    def __init__(self, config_file='conf.json'):
        self.config_file = config_file
        self.config = self.load_config_file(self.config_file)
        self.key = self.config['key']

    @staticmethod
    def load_config_file(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except IOError:
            logging.warning('{} not found.'.format(config_file))
            config = {}
        return config

    def set_last_steam_id(self):
        self.total_steam_users = self.get_total_users()
        self.last_steam_id = self.first_steam_id + self.total_steam_users

    def make_request(self, user_id, sleep_length=0, error=True):
        url = '{}?key={}&steamid={}&format=json'.format(
            self.base_url, self.key, user_id)
        r = requests.get(url)
        try:
            r.json()
            return r
        except json.decoder.JSONDecodeError as e:
            if error:
                logging.warning('Response not json.  Error: {}\n {}'.format(
                    e, r.text))
            time.sleep(sleep_length)
            return False

    @staticmethod
    def get_numbers_from_list(number_list):
        return sum([((10 ** y[0]) * y[1]) for y in number_list])

    def get_total_users(self, last_number=12, number_list=None):
        logging.info('Getting total users.')
        if not number_list:
            number_list = []
        for exponent in range(last_number, 1, -1):
            for multi in range(9, 1, -1):
                user_id = (self.first_steam_id + ((10 ** exponent) * multi) +
                           self.get_numbers_from_list(number_list))
                if self.make_request(user_id, error=False):
                    logging.info('10 to the power of {} times {} was a user. '
                                 'Number list {}'.format(exponent, multi,
                                                         number_list))
                    number_list.append((exponent, multi))
                    break
        total_users = self.get_numbers_from_list(number_list)
        return total_users

    def user_search_loop(self, search_num=None):
        if not search_num:
            search_num = self.default_search_num
        number_hits = 0
        df = pd.DataFrame()
        for x in range(search_num):
            logging.info('Search number {} of {} Hits: {}'
                         .format(x, search_num, number_hits))
            df, number_hits = self.get_random_user_df(df, number_hits)
        return df

    def get_random_user_df(self, df, number_hits=0):
        r, user_id = self.request_random_user()
        df, number_hits = self.get_df_from_response(df, r, user_id, number_hits)
        return df, number_hits

    def request_random_user(self):
        random_int = random.randint(self.first_steam_id, self.last_steam_id)
        logging.info('Searching user {}'.format(random_int))
        r = self.make_request(random_int, sleep_length=120)
        return r, random_int

    def request_random_user_wishlist(self):
        random_int = random.randint(self.first_steam_id, self.last_steam_id)
        logging.info('Searching user {}'.format(random_int))
        wish_url = ('https://store.steampowered.com/wishlist/profiles/'
                    '{}/wishlistdata/?p=0'.format(random_int))
        r = requests.get(wish_url)
        return r

    @staticmethod
    def get_df_from_response(df, r, user_id, number_hits=0):
        if r and ('response' in r.json() and r.json()['response'] and
                  'games' in r.json()['response']):
            number_hits += 1
            tdf = pd.DataFrame(r.json()['response']['games'])
            tdf['steam_id'] = user_id
            df = df.append(tdf, ignore_index=True)
        return df, number_hits

    @staticmethod
    def get_game_dict():
        url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
        r = requests.get(url)
        game_dict = r.json()['applist']['apps']['app']
        game_dict = pd.DataFrame(game_dict)
        return game_dict

    def get_data_write_df(self, search_num=None):
        self.set_last_steam_id()
        df = self.user_search_loop(search_num=search_num)
        game_dict = self.get_game_dict()
        df = df.merge(game_dict, on='appid', how='left')
        file_name = 'steam_users_{}.csv'.format(
            dt.datetime.today().date().strftime('%Y%m%d'))
        df.to_csv(os.path.join('data', file_name))


def main():
    set_log()
    steam_api = SteamApi()
    steam_api.get_data_write_df(args.loop)


if __name__ == '__main__':
    main()
