import datetime
import logging
from decimal import Decimal, ROUND_HALF_UP

from . import DAILY, MONTHLY, YEARLY
from .models import TargetDepartment, TargetJobRole, TargetEmployee
from utils import get_next_day, get_next_month, get_next_year, get_age


class TransformError(Exception):
    """
    Transform exception for all formatting errors.
    """
    pass


class Transform(object):
    """
    Transforms source objects into target objects.
    """
    def __init__(self, database, config):
        self.database = database
        self.time_interval = config['time_interval']
        self.simulate_interval = config['simulate_interval']
        self.simulate_interval_start = config['simulate_interval_start']
        self.today = datetime.date.today()
        self.tid = None  # Primary key for new date in tgt_N.dim_time
        self.exchange = None  # Instance of Exchange with exchange rate set

    def _get_latest_date(self):
        """
        Returns latest date from tgt_N.dim_time.
        """
        latest_date = None
        query = "SELECT date FROM dim_time ORDER BY date DESC LIMIT 1"
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchone()
        if row is not None:
            latest_date = row[0]
        return latest_date

    def _get_interval_date_format(self, interval_str):
        """
        Returns Python date format for the given interval.
        """
        if interval_str == DAILY:
            return "%Y-%m-%d"
        elif interval_str == MONTHLY:
            return "%Y-%m"
        elif interval_str == YEARLY:
            return "%Y"
        else:
            raise ValueError("invalid time_interval: {}".format(interval_str))

    def _get_simulation_interval(self):
        """
        Returns the start date object and the interval in a tuple for use in
        simulation.
        """
        if self.simulate_interval.lower() != "true":
            return None
        interval_str = self.time_interval
        try:
            start_date = datetime.datetime.strptime(
                self.simulate_interval_start,
                self._get_interval_date_format(interval_str)).date()
        except ValueError as err:
            raise TransformError(err)
        return (start_date, interval_str)

    def get_new_date(self):
        """
        When simulation_interval is False, this function simply returns the
        current date. Otherwise, it will return an incremented date based on
        the latest date and the given interval settings.
        """
        new_date = None

        latest_date = self._get_latest_date()
        if latest_date is not None:
            logging.debug("latest_date={}".format(latest_date))
            new_date = latest_date

        interval = self._get_simulation_interval()
        if interval is not None:
            (start_date, interval_str) = interval
            if new_date is not None:
                if interval_str == DAILY:
                    new_date = get_next_day(new_date)
                elif interval_str == MONTHLY:
                    new_date = get_next_month(new_date)
                elif interval_str == YEARLY:
                    new_date = get_next_year(new_date)
            else:
                new_date = start_date  # First simulation date
            self.today = new_date  # Today in simulation
        else:
            # Use current date when not simulating
            new_date = self.today

        new_date = new_date.strftime("%Y-%m-%d")  # To match MySQL DATE format
        logging.debug("new_date={}".format(new_date))
        return new_date

    def departments(self, source_departments, cid):
        """
        Transforms source department objects.
        """
        for department in source_departments:
            yield TargetDepartment(
                department.id,  # Reference use only, NOT INSERTED INTO DB
                department.name,
                department.did,
                cid,
                self.tid)

    def jobroles(self, source_jobroles):
        """
        Transforms source jobrole objects.
        """
        for jobrole in source_jobroles:
            yield TargetJobRole(
                jobrole.id,  # Reference use only, NOT INSERTED INTO DB
                jobrole.name)

    def _apply_exchange_rate(self, source_amount):
        """
        Applies exchange rate on the given amount, e.g. to convert it to
        an amount in base currency.
        """
        assert self.exchange is not None
        assert self.exchange.exchange_rate is not None
        if self.exchange.exchange_rate == 1:  # No conversion needed
            return source_amount
        target_amount = Decimal(source_amount) * self.exchange.exchange_rate
        logging.debug("exchange_rate={} [{}]->[{}]".format(
            self.exchange.exchange_rate, source_amount, target_amount))
        return target_amount.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

    def employees(self, source_employees, cid):
        """
        Transforms source employees objects.
        """
        for employee in source_employees:
            yield TargetEmployee(
                employee.id,  # Reference use only, NOT INSERTED INTO DB
                employee.gender,
                employee.did,
                employee.jid,
                self.tid,
                cid,
                self._apply_exchange_rate(employee.salary),
                employee.manager,
                get_age(employee.dob, self.today))
