import logging


class Load(object):
    """
    Loads objects into the given target database.
    """
    def __init__(self, database):
        self.database = database

    def date(self, date, time_interval):
        """
        Inserts new date into tgt_N.dim_time table. The given date must be a
        string in yyyy-mm-dd format. This function returns the primary key
        for the inserted date.
        """
        query = ("INSERT INTO dim_time (date, time_interval) VALUE ('{}', "
                 "'{}')".format(date, time_interval.upper()))
        self.database.cursor.execute(query)
        self.database.conn.commit()
        return self.database.cursor.lastrowid

    def _clean(self, data):
        """
        Converts None to NULL for insertion into MySQL database.
        """
        if data is None:
            return "NULL"
        return data

    def departments(self, departments):
        """
        Loads department objects into tgt_N.dim_department table.
        """
        departments_map = {}
        for department in departments:
            name = department.name
            did = department.did
            if did is not None:
                did = departments_map[department.did]
            else:
                did = self._clean(did)
            cid = department.cid
            tid = department.tid
            query = ("INSERT INTO dim_department (name, did, cid, tid) VALUE "
                     "('{}', {}, {}, {})".format(name, did, cid, tid))
            logging.debug(query)
            self.database.cursor.execute(query)
            self.database.conn.commit()
            departments_map[department.id] = self.database.cursor.lastrowid
        return departments_map

    def _get_jobrole(self, name):
        """
        Returns the row from tgt_N.dim_jobrole table that has the same job
        role's name.
        """
        query = "SELECT * FROM dim_jobrole WHERE name = '{}'".format(name)
        logging.debug(query)
        self.database.cursor.execute(query)
        row = self.database.cursor.fetchone()
        return row

    def jobroles(self, jobroles):
        """
        Loads jobrole objects into tgt_N.dim_jobrole table.
        """
        jobroles_map = {}
        for jobrole in jobroles:
            name = jobrole.name
            _jobrole = self._get_jobrole(name)
            if _jobrole is not None:
                jobroles_map[jobrole.id] = _jobrole[0]
            else:
                query = "INSERT INTO dim_jobrole (name) VALUE ('{}')".format(
                    name)
                logging.debug(query)
                self.database.cursor.execute(query)
                self.database.conn.commit()
                jobroles_map[jobrole.id] = self.database.cursor.lastrowid
        return jobroles_map

    def employees(self, employees, departments_map, jobroles_map):
        """
        Loads employee objects into tgt_N.fact_employee table.
        """
        employees_map = {}
        for employee in employees:
            gender = employee.gender
            did = departments_map[employee.did]
            jid = jobroles_map[employee.jid]
            tid = employee.tid
            cid = employee.cid
            salary = employee.salary
            manager = employee.manager
            age = employee.age
            query = ("INSERT INTO fact_employee (gender, did, jid, tid, cid, "
                     "salary, manager, age) VALUE "
                     "('{}', {}, {}, {}, {}, {}, {}, {})".format(gender, did,
                     jid, tid, cid, salary, manager, age))
            logging.debug(query)
            self.database.cursor.execute(query)
            self.database.conn.commit()
            employees_map[employee.id] = self.database.cursor.lastrowid
        return employees_map
