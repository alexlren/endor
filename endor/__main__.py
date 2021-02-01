import argparse
import configparser
import logging
import sys
import time
import yfinance as yf
from appdirs import user_config_dir
from os import path

app_name = 'endor'
# Logger
log = logging.getLogger(__name__)

def poll_data(settings, args):
    symbols = settings.sections()
    interval = args.interval
    period = args.period

    if len(symbols) == 0:
        log.error('No symbols found, add settings.init file')
        return 1
    try:
        while True:
            tickers = ' '.join(symbols)
            log.debug(f'retrieve data for {tickers} - interval = {interval}')
            data = yf.download(tickers = tickers, interval = interval, period = period, group_by = 'tickers',
                               auto_adjust = True, prepost = True, threads = True)
            print(data)
            time.sleep(args.refresh)
    except KeyboardInterrupt:
        log.debug('interrupted')
        return 0

def main():
    parser = argparse.ArgumentParser(prog = app_name)
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='output debug log messages to stderr')
    parser.add_argument(
        '-i', '--interval', type=str,
        choices=['1m', '2m', '5m', '15m', '30m',
                 '60m', '90m', '1h', '1d', '5d',
                 '1wk', '1mo', '3mo'],
        default='1m',
        help='fetch data by interval')
    parser.add_argument(
        '-p', '--period', type=str,
        choices=['1d', '5d', '1mo', '3mo','6mo',
                 '1y', '2y', '5y', '10y', 'ytd', 'max'],
        default='1d',
        help='period of time to look at')
    parser.add_argument(
        '-r', '--refresh', type=int,
        default=60,
        help='refresh time in secs')

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format='%(relativeCreated)d ms [%(levelname)s:%(name)s] %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    settings = configparser.ConfigParser()
    settings_dir = user_config_dir(app_name)
    settings_file = path.join(settings_dir, 'settings.ini')

    log.debug(f'reading config file from {settings_file}')
    settings.read(settings_file)
    return poll_data(settings, args)

if __name__ == '__main__':
    sys.exit(main())
