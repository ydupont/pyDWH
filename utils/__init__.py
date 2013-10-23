import calendar
import datetime
import logging
import sys
from ConfigParser import ConfigParser


def read_config(filepath):
    """
    Returns config with key-value pairs from configuration file.
    """
    config = {
        'sources': {},
        'target': {},
        'general': {},
    }
    conf = ConfigParser()
    conf.read(filepath)
    sections = conf.sections()
    for section in sections:
        if section.startswith('source'):
            config['sources'][section] = {}
            sect = config['sources'][section]
        else:
            config[section] = {}
            sect = config[section]
        for option in conf.options(section):
            sect[option] = conf.get(section, option)
    return config


def setup_logger(filename, debug):
    """
    Initializes logger.
    """
    sys.stderr.write("Writing output to logfile: {}\n".format(filename))
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    format = ("%(levelname)s %(asctime)s %(message)s")
    logging.basicConfig(level=level, format=format, filename=filename,
                        filemode="w")


def get_next_day(current_date):
    """
    Returns next day's datetime.date object based on current date.
    """
    return current_date + datetime.timedelta(days=1)


def get_next_month(current_date):
    """
    Returns next month's datetime.date object based on current date.
    """
    month = current_date.month
    year = current_date.year + month / 12
    month = month % 12 + 1
    day = min(current_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def get_next_year(current_date):
    """
    Returns next year's datetime.date object based on current date.
    """
    next_date = None
    try:
        next_date = current_date.replace(year=current_date.year + 1)
    except ValueError:
        # This happens if date falls on 29th Feb and the current year is
        # not a leap year.
        next_date = current_date.replace(year=current_date.year + 1,
                                         day=current_date.day - 1)
    return next_date


def get_age(dob, current_date):
    """
    Returns person's age as of current date given the date of birth.
    """
    try:
        bday = dob.replace(year=current_date.year)
    except ValueError:
        # This happens if dob falls on 29th Feb and the current year is
        # not a leap year.
        bday = dob.replace(year=current_date.year, day=dob.day - 1)
    if bday > current_date:
        age = current_date.year - dob.year - 1
    else:
        age = current_date.year - dob.year
    return age
