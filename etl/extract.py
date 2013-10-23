from .models import SourceDepartment, SourceJobRole, SourceEmployee


class Extract(object):
    """
    Extracts rows data from the given source database.
    """
    def __init__(self, database):
        self.database = database

    def departments(self):
        """
        Returns department objects in a generator.
        """
        self.database.cursor.execute("SELECT * FROM department")
        rows = self.database.cursor.fetchall()
        for row in rows:
            yield SourceDepartment(*row)

    def jobroles(self):
        """
        Returns jobrole objects in a generator.
        """
        self.database.cursor.execute("SELECT * FROM jobrole")
        rows = self.database.cursor.fetchall()
        for row in rows:
            yield SourceJobRole(*row)

    def employees(self):
        """
        Returns employee objects in a generator.
        """
        self.database.cursor.execute("SELECT * FROM employee")
        rows = self.database.cursor.fetchall()
        for row in rows:
            yield SourceEmployee(*row)
