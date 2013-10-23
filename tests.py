import unittest
from etl.exchange import Exchange, ExchangeError


class ExchangeTestCase(unittest.TestCase):
    """
    Test cases for exchange module.
    """

    def setUp(self):
        config = {
            'base_currency': "EUR",
            'exchange_rate_api': ("http://finance.yahoo.com"
                                  "/d/quotes.csv?f=sl1&s=__DATA__=X"),
        }
        self.exchange = Exchange(config)

    def test_set_exchange_rate(self):
        """
        Tests that exchange rate gets reset to 1 having it set to foreign
        exchange rate earlier.
        """
        self.exchange.set_exchange_rate(source_currency="EUR")
        self.assertEqual(self.exchange.exchange_rate, 1)

        self.exchange.set_exchange_rate(source_currency="USD")
        self.assertFalse(self.exchange.exchange_rate == 1)

        self.exchange.set_exchange_rate(source_currency="GBP")
        self.assertFalse(self.exchange.exchange_rate == 1)

        self.exchange.set_exchange_rate(source_currency="EUR")
        self.assertEqual(self.exchange.exchange_rate, 1)


if __name__ == '__main__':
    unittest.main()
