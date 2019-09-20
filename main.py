import sys
import logging
import argparse
import steam.export as exp
import steam.steamapi as api


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
parser.add_argument('--nopull', action='store_true')
parser.add_argument('--exp', choices=['all', 'db', 'ftp'])
args = parser.parse_args()


def main():
    set_log()
    if not args.nopull:
        steam_api = api.SteamApi()
        steam_api.get_data_write_df(args.loop)
    if args.exp:
        exp_class = exp.ExportHandler()
        exp_class.export_loop(args.exp)


if __name__ == '__main__':
    main()
