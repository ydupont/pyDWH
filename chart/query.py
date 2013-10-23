import logging
from MySQLdb import ProgrammingError
from . import MEDIAN, TOTAL, AGE, COMPANY, GENDER, JOBROLE, MANAGER


class QueryError(Exception):
    """
    Query exception for all MySQL query errors.
    """
    pass


class Query(object):
    """
    Performs database queries to fetch all the required lines data in order to
    generate a chart.
    """
    def __init__(self, database, chart):
        self.database = database
        self.chart = chart

    def _split_line_range(self, line_range):
        """
        Splits a line range into a tuple representing start and end of the
        range. This is typically used for age range.
        """
        line_range = line_range.split("-")
        if len(line_range) > 1:
            (start, end) = line_range
        else:
            start = line_range[0]
            end = start
        return (start, end)

    def _get_tables(self):
        """
        Returns a list of tables that forms the FROM clause for a query given
        the data type.
        """
        if self.chart['data_type'] == JOBROLE:
            return "fact_employee e, dim_time d, dim_jobrole j"
        return "fact_employee e, dim_time d"

    def _get_time_limit(self):
        """
        Returns a time limit string that forms the WHERE clause for a query
        given the x-axis inputs.
        """
        x_unit = self.chart['x']['unit'].upper()  # x-axis for time
        x_limit = self.chart['x']['limit']  # (start, end) or None
        time_limit = "e.tid = d.id AND d.time_interval = '{}'".format(x_unit)
        if x_limit is not None:
            time_limit += " AND d.date >= '{}' AND d.date <= '{}'".format(
                x_limit[0], x_limit[1])
        return time_limit

    def _get_data_limit(self, line_range):
        """
        Returns a data limit string that forms the WHERE clause for a query
        given the data label.
        """
        data_limit = ""
        data_type = self.chart['data_type']
        if data_type == AGE:
            (start, end) = self._split_line_range(line_range)
            data_limit = "e.age >= {} AND e.age <= {}".format(start, end)
        elif data_type == COMPANY:
            data_limit = "e.cid = {}".format(int(line_range))
        elif data_type == GENDER:
            data_limit = "e.gender = '{}'".format(line_range.upper())
        elif data_type == JOBROLE:
            data_limit = "e.jid = j.id AND j.name = '{}'".format(line_range)
        elif data_type == MANAGER:
            data_limit = "e.manager = {}".format(int(line_range))
        return data_limit

    def _get_data_select(self, context):
        """
        Returns a select statement that forms a joinable query given the
        unit for y-axis, i.e.  median or total.
        """
        query = ""
        if self.chart['y']['unit'] == MEDIAN:
            query = (
                "(SELECT date AS line{idx}_date, "
                "AVG(salary) AS line{idx}_value "
                "FROM ( "
                "SELECT t1.row, t1.salary, t1.date FROM ( "
                "SELECT IF(@prev != date, @rownum := 1, @rownum := @rownum + 1) AS row, @prev := date AS date, salary "
                "FROM ( "
                "SELECT d.date, e.salary "
                "FROM {tables} "
                "WHERE {data_limit} AND {time_limit} "
                "ORDER BY date, salary "
                ") ordered, (SELECT @rownum := 0, @prev := NULL) reset "
                ") AS t1 INNER JOIN "
                "( "
                "SELECT COUNT(*) AS total_rows, d.date AS date "
                "FROM {tables} "
                "WHERE {data_limit} AND {time_limit} "
                "GROUP BY date "
                ") AS t2 "
                "ON t1.date = t2.date "
                "AND t1.row >= t2.total_rows / 2 AND t1.row <= ((t2.total_rows / 2) + 1) "
                ") median "
                "GROUP BY date ORDER BY date) line{idx} ")
        elif self.chart['y']['unit'] == TOTAL:
            query = (
                "(SELECT d.date AS line{idx}_date, "
                "SUM(e.salary) AS line{idx}_value "
                "FROM {tables} "
                "WHERE {data_limit} AND {time_limit} "
                "GROUP BY date ORDER BY date) line{idx} ")
        return query.format(idx=context['idx'],
                            tables=context['tables'],
                            data_limit=context['data_limit'],
                            time_limit=context['time_limit'])

    def get_data_rows(self, line_ranges):
        """
        Returns data rows for use in rendering the chart given the line ranges.
        """
        left_column = "COALESCE("  # Header for first column
        right_columns = ""  # Headers for subsequent columns
        joins = " "
        tables = self._get_tables()
        time_limit = self._get_time_limit()

        for idx, line_range in enumerate(line_ranges, 1):
            data_limit = self._get_data_limit(line_range)

            joins += self._get_data_select({
                'idx': idx,
                'tables': tables,
                'data_limit': data_limit,
                'time_limit': time_limit,
            })

            if idx > 1:
                joins += "ON line{}_date = line{}_date ".format(idx - 1, idx)
            if idx != len(line_ranges):
                joins += "LEFT JOIN "

            left_column += "line{}_date".format(idx)
            if idx < len(line_ranges):
                left_column += ", "
            else:
                left_column += ") AS date,"

            right_columns += "line{}_value".format(idx)
            if idx < len(line_ranges):
                right_columns += ", "

        query = "SELECT {} {} FROM".format(left_column, right_columns) + joins
        logging.debug("query={}".format(query))

        try:
            self.database.cursor.execute(query)
        except ProgrammingError as err:
            raise QueryError(err)
        rows = self.database.cursor.fetchall()

        logging.debug("rows={}".format(rows))
        return rows
