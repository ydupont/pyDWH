#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Callable script for etl module.
"""

import json
import logging
import optparse
import os
import sys

from db.database import Database, DatabaseError
from etl.exchange import Exchange, ExchangeError
from etl.extract import Extract
from etl.load import Load
from etl.transform import Transform, TransformError
from utils import read_config, setup_logger

DEFAULT_USAGE_TEXT = ("""Usage: %prog [options]
Script to perform extract, transform and load flow.
Example: %prog --config=config.cfg --verbose""")


def run_source_etl(source, source_settings, transform, load):
    """
    Commits the extract, transform and load flow for the given source.
    """
    cid = int(source_settings['company_id'])
    logging.debug("cid={}".format(cid))
    try:
        source_database = Database(source_settings)
    except DatabaseError as err:
        sys.stderr.write("ERROR: {}\n".format(err))
        return 1
    extract = Extract(source_database)

    source_departments = extract.departments()
    target_departments = transform.departments(source_departments, cid)
    departments_map = load.departments(target_departments)
    logging.debug("departments_map={}".format(
        json.dumps(departments_map, indent=2)))

    source_jobroles = extract.jobroles()
    target_jobroles = transform.jobroles(source_jobroles)
    jobroles_map = load.jobroles(target_jobroles)
    logging.debug("jobroles_map={}".format(
        json.dumps(jobroles_map, indent=2)))

    source_employees = extract.employees()
    target_employees = transform.employees(source_employees, cid)
    employees_map = load.employees(target_employees, departments_map,
                                   jobroles_map)
    logging.debug("employees_map={}".format(
        json.dumps(employees_map, indent=2)))

    logging.info("{} employees added from {}".format(
        len(employees_map), source))

    source_database.close()
    return 0


def run_etl(config):
    """
    Manages extract, transform and load flow. The flow imports rows data
    from source databases, map the data into Python objects and finally
    loads the objects into target database.
    """
    try:
        target_database = Database(config['target'])
    except DatabaseError as err:
        sys.stderr.write("ERROR: {}\n".format(err))
        return 1

    # Prep transform
    transform = Transform(target_database, config['general'])
    try:
        new_date = transform.get_new_date()
    except TransformError as err:
        sys.stderr.write("ERROR: {}\n".format(err))
        return 1

    # Prep load
    load = Load(target_database)
    # Commits new date
    tid = load.date(new_date, config['general']['time_interval'])
    transform.tid = tid
    logging.debug("tid={}".format(tid))

    # Instantiates a currency converter using base currency as target currency
    exchange = Exchange(config['general'])
    transform.exchange = exchange

    # Commits ETL by source
    retcode = 0
    for source, source_settings in config['sources'].items():
        logging.debug("source={} source_settings={}".format(
            source, source_settings))
        source_currency = source_settings['currency']
        try:
            # This fetches external data so it's important to fail early
            exchange.set_exchange_rate(source_currency=source_currency)
        except ExchangeError as err:
            sys.stderr.write("ERROR: {}\n".format(err))
            return 1
        retcode += run_source_etl(source, source_settings, transform, load)

    target_database.close()

    return retcode


def main(argv):
    """
    Entry point for etl module.
    """
    option_parser = optparse.OptionParser(usage=DEFAULT_USAGE_TEXT)
    option_parser.add_option("-c", "--config", dest="config",
                             default="config.cfg", help="Configuration file")
    option_parser.add_option("-v", "--verbose", dest="verbose",
                             action="store_true", default=False,
                             help="Show verbose output")
    options, _ = option_parser.parse_args(argv)

    if not os.path.exists(options.config):
        sys.stderr.write("ERROR: {} does not exist\n".format(options.config))
        option_parser.print_help()
        return 1
    config = read_config(options.config)

    log_dir = config['general']['log_dir']
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    filename = os.path.join(log_dir, __file__.replace(".py", ".log"))
    setup_logger(filename, options.verbose)
    logging.debug("config={}".format(json.dumps(config, indent=2)))

    retcode = run_etl(config)
    return retcode


if __name__ == '__main__':
    sys.exit(main(sys.argv))