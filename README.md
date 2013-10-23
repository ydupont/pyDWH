# pyDWH
pyDWH is a show case Date Warehouse implementation for the 101companies project (http://101companies.org).
It consists of two different components:

* ETL
extracts data from source database(s), transforms and loads it into the target database

* Chart generator
generates charts based on data of the target database

## Features
* Support for multiple data sources
* Live conversion for the currencies of the data sources using Yahoo! Finance API (R)
* Dynamic and configurable data history (daily, monthly, yearly)
* Adjustable chart generation using Google Chart API
* more

## Modules
### etl
The etl module handles all the database queries to get the source data via etl.extract. All models that map to tables in the source database are defined in etl.models. 
etl.transform is responsible in transforming source data that maps to tables in the target database. etl.load saves the transformed data into the target database.

### db
The db module contains the Database class. When instantiated, the Database object establishes connection to a MySQL database and exposes the cursor and connection 
attributes for use in querying the database.

### chart
The chart module handles all the database queries to get chart data via its Query class. The Render class requires the chart data in order to render the template HTML 
file with the help of Jinja. The rendered HTML file uses Google Chart API to generate chart.

### utils
The utils module contains various helper functions that do not fit in a particular module.

## Requirements
* Python >= 2.7.1
* MySQL-python (http://sourceforge.net/projects/mysql-python)
* Jinja2 >= 2.7 (http://jinja.pocoo.org/)
* MySQL Client >= 5.0
* MySQL Server >= 5.0
* Internet access (at least while opening the generated charts)

## Preparation
Create the source and target databases:

    mysql> CREATE DATABASE src_1;
    mysql> CREATE DATABASE src_2;
    mysql> CREATE DATABASE tgt;

NOTE: Grant privileges in case you don´t want to use the root user.
You can use "n" source databases.

Load source- and target database schema:

    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_1 < sql/schema/src.sql
    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_2 < sql/schema/src.sql
    $ mysql -u <USERNAME> -p -h <HOSTNAME> tgt < sql/schema/tgt.sql

Populate the databases on your own or using the sample data:

    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_1 < sql/sample/src_1/src_1_1.sql
    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_2 < sql/sample/src_2/src_2_1.sql

## Execute
Please check the configuration file (config.cfg) and adjust it according to your environment.
You may add new "source" sections.

In case you want to use the ETL in production mode you will have to install a new cronjob with the following command:

    $ python run_etl.py -c config.cfg
    (please ensure that you are in the proper directory)

In case you want to use the ETL in simulation mode you will have to change the according options in the configuration files and
run the ETL as well as the database updates manually. You can do it with the packaged sample SQL files:

    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_1 < sql/sample/src_1/src_1_1.sql
    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_2 < sql/sample/src_2/src_2_1.sql
    $ python run_etl.py -c config.cfg

    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_1 < sql/sample/src_1/src_1_2.sql
    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_2 < sql/sample/src_2/src_2_2.sql
    $ python run_etl.py -c config.cfg

    ........................................

    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_1 < sql/sample/src_1/src_1_10.sql
    $ mysql -u <USERNAME> -p -h <HOSTNAME> src_2 < sql/sample/src_2/src_2_10.sql
    $ python run_etl.py -c config.cfg


Now you can generate a chart. I.e.:

    $ python generate_chart.py -x time -X yearly -y salary -Y median -d company -D 1,2

## Usage

    $ generate_chart.py --help
      Usage: generate_chart.py [options]
      Script to generate chart using data from target database.
      Examples:
      generate_chart.py -x time -X yearly -y salary -Y median -d age -D 26-35,36-45
      generate_chart.py -x time -X 2000,2010 -y salary -Y median -d jobrole -D "Project Manager"
      See generate_chart.py --help for supported options.
      
      Options:
        -h, --help            			show this help message and exit
        -c CONFIG, --config=CONFIG		Configuration file
        -v, --verbose         			Show verbose output
        -x X_AXIS, --x_axis=X_AXIS		Label for x-axis: time
        -X X_OUTPUT, --x_output=X_OUTPUT	Unit for x-axis. time: daily, month, yearly or range
                        			2000,2003. Range for time is separated by comma to
                        			allow daily range such as -X 2000-01-01,2003-08-20
        -y Y_AXIS, --y_axis=Y_AXIS              Label for y-axis: salary
        -Y Y_OUTPUT, --y_output=Y_OUTPUT	Unit for y-axis. salary: median or total
        -d DATA_TYPE, --data_type=DATA_TYPE	Data type for plotted lines: age, company, gender,
                        			jobrole or manager
        -D DATA_OUTPUT, --data_output=DATA_OUTPUT
						Unit for plotted lines. age: comma-separated list of
                        			ages or ranges, company: comma-separated list of IDs,
                        			gender: comma-separated list (male,female, undefined
                        			or empty for all), jobrole: comma-separated list of
                        			job roles, manager: comma-separated list (true,false)

    $ run_etl.py --help
      Usage: run_etl.py [options]
      Script to perform extract, transform and load flow.
      Example: run_etl.py --config=config.cfg --verbose
      See run_etl.py --help for supported options.

      Options:
        -h, --help            			show this help message and exit
        -c CONFIG, --config=CONFIG		Configuration file
        -v, --verbose         			Show verbose output


