import logging
import urllib2
from decimal import Decimal

# Supported currencies based on the list from European Central Bank:
# http://www.ecb.int/stats/exchange/eurofxref/html/index.en.html
CURRENCIES = [
    "AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP",
    "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "LTL", "LVL",
    "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD",
    "THB", "TRY", "USD", "ZAR"
]


class ExchangeError(Exception):
    """
    Exchange exception for all conversion errors.
    """
    pass


class Exchange(object):
    """
    Performs currency conversion using an external API specified in the
    configuration file.
    """
    def __init__(self, config):
        self.base_currency = config['base_currency']
        assert self.base_currency in CURRENCIES
        self.exchange_rate_api = config['exchange_rate_api']
        self.exchange_rate = None

    def set_exchange_rate(self, source_currency, target_currency=None):
        """
        Fetches current exchange rate from Yahoo! Finance API and set
        instance's exchange_rate with respect to the given target currency.
        """
        if target_currency is None:
            target_currency = self.base_currency

        if source_currency == target_currency:
            # Same currency, i.e. no conversion
            self.exchange_rate = 1
            return

        if source_currency not in CURRENCIES:
            raise ExchangeError("unknown currency: {}".format(source_currency))
        if target_currency not in CURRENCIES:
            raise ExchangeError("unknown currency: {}".format(target_currency))

        data = "{}{}".format(source_currency, target_currency)
        url = self.exchange_rate_api.replace("__DATA__", data)
        response = ""
        logging.debug("url={}".format(url))
        request = urllib2.Request(url=url)
        try:
            response = urllib2.urlopen(request).read()
        except (urllib2.HTTPError, urllib2.URLError) as err:
            raise ExchangeError(err)
        response = response.strip()

        logging.debug("response={}".format(response))
        if data not in response:
            raise ExchangeError("invalid data from {}: {}".format(url, data))

        exchange_rate = response.split(",", 1)[1]
        self.exchange_rate = Decimal(exchange_rate)
