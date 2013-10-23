import datetime
import logging
import os
from decimal import Decimal, ROUND_HALF_UP
from jinja2 import Environment, PackageLoader


class Render(object):
    """
    Renders chart with output written into HTML file given the chart data in
    Python dict.
    """
    def __init__(self, chart, config):
        self.chart = chart
        self.config = config
        self.env = Environment(loader=PackageLoader("chart", "templates"),
                               trim_blocks=True, lstrip_blocks=True)

    def _get_filepath(self, chart_dir):
        """
        Returns filepath to which the HTML output containing the chart will
        be written to. Format: chart_X-Y-DATA_YYYYMMDD.html
        """
        x = self.chart['x']['label']
        y = self.chart['y']['label']
        data_type = self.chart['data_type']
        date = datetime.date.today().strftime("%Y%m%d")
        filename = "chart_{}-{}-{}_{}.html".format(x, y, data_type, date)
        filepath = os.path.join(chart_dir, filename)
        return filepath

    def _format_row(self, row):
        """
        Formats column data in a row according to its data type.
        """
        formatted_row = []
        for column in row:
            if column is None:
                column = "null"  # JavaScript's None
            elif isinstance(column, float):
                column = Decimal(column)  # Currency
                column = column.quantize(Decimal(".01"),
                                         rounding=ROUND_HALF_UP)
            formatted_row.append(column)
        return formatted_row

    def render(self):
        """
        Renders the chart data on top of the given template file and writes
        the rendered output to a HTML file.
        """
        chart_dir = self.config['chart_dir']
        if not os.path.exists(chart_dir):
            os.mkdir(chart_dir)

        template = self.env.get_template("chart.html")
        formatted_rows = []
        for row in self.chart['data_rows']:
            formatted_rows.append(self._format_row(row))
        self.chart['data_rows'] = formatted_rows
        context = {
            'chart': self.chart,
            'base_currency': self.config['base_currency'],
        }
        html = template.render(context)
        logging.debug("html=\n{}".format(html))

        filepath = self._get_filepath(chart_dir)
        logging.debug("filepath={}".format(filepath))

        open(filepath, "w").write(html)
        logging.info("{} generated".format(filepath))

        return 0
