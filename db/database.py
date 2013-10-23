from MySQLdb import connect, OperationalError


class DatabaseError(Exception):
    """
    Database exception for all MySQL connection errors.
    """
    pass


class Database(object):
    """
    MySQL connection instance.
    [src_1..N]
    department: id | name | did
    jobrole: id | name
    employee: id | name | address | salary | manager | did | jid | gender | dob

    [tgt_1]
    dim_time: id | date | time_interval
    dim_department: id | name | did | cid | tid
    dim_jobrole: id | name
    fact_employee: id | gender | did | jid | tid | cid | salary | manager | age
    """
    def __init__(self, settings):
        """
        Connects to database.
        """
        db_host = settings.get('db_host', 'localhost')
        db_user = settings.get('db_user', '')
        db_pass = settings.get('db_pass', '')
        db_name = settings.get('db_name', '')
        db_port = int(settings.get('db_port', '3306'))
        try:
            self.conn = connect(db_host, db_user, db_pass, db_name, db_port)
        except OperationalError as err:
            raise DatabaseError(err)
        self.cursor = self.conn.cursor()

    def close(self):
        """
        Closes the database connection.
        """
        self.cursor.close()
        self.conn.close()
