#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to generate chart using data from target database.
"""

import datetime
import json
import logging
import optparse
import os
import re
import sys

from chart import (TIME, SALARY, MEDIAN, TOTAL, AGE, COMPANY, GENDER,
                   JOBROLE, MANAGER)
from chart.query import Query, QueryError
from chart.render import Render
from db.database import Database, DatabaseError
from etl import DAILY, MONTHLY, YEARLY
from utils import read_config, setup_logger, get_next_month, get_next_year

DEFAULT_USAGE_TEXT = ("""Usage: %prog [options]
Script to generate chart using data from target database.
Example: %prog -x time -X yearly -y salary -Y median -d age -D 26-35,36-45
See %prog --help for supported options.""")


class ChartInputError(Exception):
    """
    Input exception for all user input errors.
    """
    pass


def get_x_axis(x_output):
    """
    Remaps value of --x_output into its unit and limit to construct the x-axis.
    """
    x_output = x_output.lower()
    if x_output in [DAILY, MONTHLY, YEARLY]:
        return (x_output, None)  # No limit

    x_limit = x_output.split(",")
    if len(x_limit) > 1:
        (start, end) = x_limit
    else:
        start = x_limit[0]
        end = start

    if re.match(r'\d{4}-\d{2}-\d{2}', start):
        x_unit = DAILY
        date_format = "%Y-%m-%d"
    elif re.match(r'\d{4}-\d{2}', start):
        x_unit = MONTHLY
        date_format = "%Y-%m"
    else:
        x_unit = YEARLY  # Default: yearly
        date_format = "%Y"

    try:
        start = datetime.datetime.strptime(start, date_format).date()
        end = datetime.datetime.strptime(end, date_format).date()
    except ValueError:
        raise ChartInputError("invalid date in {}".format(x_output))

    # Adjusts end's date to the lastest date of the end's month or year
    if x_unit == MONTHLY:
        end = get_next_month(end) - datetime.timedelta(days=1)
    elif x_unit == YEARLY:
        end = get_next_year(end) - datetime.timedelta(days=1)
    logging.debug("start={} end={}".format(start, end))

    x_limit = (str(start), str(end))
    return (x_unit, x_limit)


def get_lines(data_type, data_output):
    """
    Converts --data_output into list of lines to plot on the chart.
    """
    if data_type == MANAGER:
        data_output = data_output.replace("true", "1").replace("false", "0")
    lines = data_output.split(",")
    return lines


def generate_chart(config, options):
    """
    Manages chart generation flow. This flow imports rows data from target
    database and map them into Python dict ready for use in rendering chart
    based on the given options.
    """
    try:
        database = Database(config['target'])
    except DatabaseError as err:
        sys.stderr.write("ERROR: {}\n".format(err))
        return 1

    try:
        (x_unit, x_limit) = get_x_axis(options.x_output)
    except ChartInputError as err:
        sys.stderr.write("ERROR: {}\n".format(err))
        return 1

    lines = get_lines(options.data_type, options.data_output)
    chart = {
        'x': {'label': options.x_axis, 'unit': x_unit, 'limit': x_limit},
        'y': {'label': options.y_axis, 'unit': options.y_output},
        'data_type': options.data_type,
        'lines': lines,
    }
    logging.debug("chart={}".format(json.dumps(chart, indent=2)))

    query = Query(database, chart)
    try:
        chart['data_rows'] = query.get_data_rows(lines)
    except QueryError as err:
        sys.stderr.write("ERROR: {}\n".format(err))
        return 1

    render = Render(chart, config['general'])
    retcode = render.render()

    return retcode


def main(argv):
    """
    Entry point for chart generation.
    """
    option_parser = optparse.OptionParser(usage=DEFAULT_USAGE_TEXT)
    option_parser.add_option("-c", "--config", dest="config",
                             default="config.cfg", help="Configuration file")
    option_parser.add_option("-v", "--verbose", dest="verbose",
                             action="store_true", default=False,
                             help="Show verbose output")

    option_parser.add_option("-x", "--x_axis", type="choice",
                             choices=[TIME],
                             help="Label for x-axis: time")

    option_parser.add_option("-X", "--x_output", dest="x_output",
                             help="Unit for x-axis. "
                             "time: daily, month, yearly or range 2000,2003. "
                             "Range for time is separated by comma to allow "
                             "daily range such as -X 2000-01-01,2003-08-20")

    option_parser.add_option("-y", "--y_axis", type="choice",
                             choices=[SALARY],
                             help="Label for y-axis: salary")

    option_parser.add_option("-Y", "--y_output", type="choice",
                             choices=[MEDIAN, TOTAL],
                             help="Unit for y-axis. salary: median or total")

    option_parser.add_option("-d", "--data_type", type="choice",
                             choices=[AGE, COMPANY, GENDER, JOBROLE, MANAGER],
                             help="Data type for plotted lines: "
                             "age, company, gender, jobrole or manager")

    option_parser.add_option("-D", "--data_output", dest="data_output",
                             help="Unit for plotted lines. "
                             "age: comma-separated list of ages or ranges, "
                             "company: comma-separated list of IDs, "
                             "gender: comma-separated list (male,female, "
                             "undefined or empty for all), "
                             "jobrole: comma-separated list of job roles, "
                             "manager: comma-separated list (true,false)")

    options, _ = option_parser.parse_args(argv)
    error = ""
    if not options.x_axis:
        error = "--x_axis is required"
    if not options.x_output:
        error = "--x_output is required"
    if not options.y_axis:
        error = "--y_axis is required"
    if not options.y_output:
        error = "--y_output is required"
    if not options.data_type:
        error = "--data_type is required"
    if not options.data_output:
        error = "--data_output is required"
    if error:
        sys.stderr.write("ERROR: {}\n".format(error))
        option_parser.print_help()
        return 1

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

    retcode = generate_chart(config, options)
    return retcode


if __name__ == '__main__':
    sys.exit(main(sys.argv))
