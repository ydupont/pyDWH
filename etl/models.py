"""
Each model maps to a table in the database.
"""


class SourceDepartment(object):
    """
    Represents a row data in src_N.department table:
    id, name, did
    """
    def __init__(self, *args):
        assert len(args) == 3
        self.id = args[0]
        self.name = args[1]
        self.did = args[2]


class SourceJobRole(object):
    """
    Represents a row data in src_N.jobrole table:
    id, name
    """
    def __init__(self, *args):
        assert len(args) == 2
        self.id = args[0]
        self.name = args[1]


class SourceEmployee(object):
    """
    Represents a row data for src_N.employee table:
    id, name, address, salary, manager, did, jid, gender, dob
    """
    def __init__(self, *args):
        assert len(args) == 9
        self.id = args[0]
        self.name = args[1]
        self.address = args[2]
        self.salary = args[3]
        self.manager = args[4]
        self.did = args[5]
        self.jid = args[6]
        self.gender = args[7]
        self.dob = args[8]


class TargetDepartment(object):
    """
    Represents a row data in tgt_N.dim_department table:
    id, name, did, cid, tid
    """
    def __init__(self, *args):
        assert len(args) == 5
        self.id = args[0]
        self.name = args[1]
        self.did = args[2]
        self.cid = args[3]
        self.tid = args[4]


class TargetJobRole(object):
    """
    Represents a row data in tgt_N.dim_jobrole table:
    id, name
    """
    def __init__(self, *args):
        assert len(args) == 2
        self.id = args[0]
        self.name = args[1]


class TargetEmployee(object):
    """
    Represents a row data for tgt_N.fact_employee table:
    id, gender, did, jid, tid, cid, salary, manager, age
    """
    def __init__(self, *args):
        assert len(args) == 9
        self.id = args[0]
        self.gender = args[1]
        self.did = args[2]
        self.jid = args[3]
        self.tid = args[4]
        self.cid = args[5]
        self.salary = args[6]
        self.manager = args[7]
        self.age = args[8]
