import sys
from dataclasses import dataclass

"""
Event,Date,Center Referee,Age Category,Lifter,Body Weight (Kg),Snatch Lift 1,Snatch Lift 2,Snatch Lift 3,C&J Lift 1,C&J Lift 2,C&J Lift 3,Total,Sinclair
European Masters 2021,2021-10-17,Eddie Halstead,Men's Masters (35-39) 73Kg,Neil Dougan,71.80,80,-86,86,100,106,112,198,257
"""


@dataclass
class LifterResult(object):
    event: str
    date: str
    referee: str
    age_cat: str
    lifter: str
    bodyweight: float
    sn_1: int
    sn_2: int
    sn_3: int
    cj_1: int
    cj_2: int
    cj_3: int
    total: int
    sinclair: int
    expected_entry_len: int = 14

    def __init__(self, db_line: list):
        if len(db_line) != self.expected_entry_len:
            sys.exit(f"Entry not formatted correctly...\n{db_line}")
        self.list_t = db_line
        self.event = db_line[0]
        self.lifter = db_line[4]
        self.bodyweight = float(db_line[5])
        self.sn_1 = int(db_line[6])
        self.sn_2 = (db_line[7])
        self.sn_3 = (db_line[8])
        self.cj_1 = (db_line[9])
        self.cj_2 = (db_line[10])
        self.cj_3 = (db_line[11])
        self.lift_attempts = [self.sn_1, self.sn_2, self.sn_3, self.cj_1, self.cj_2, self.cj_3]

    def first_snatch(self):
        return self.sn_1
        """        try:
                    if self.sn_1 > 1:
                        return self.sn_1 / self.bodyweight
                except TypeError:
                    print(self.sn_1)"""

    def lift_increments(self):
        try:
            first_jump = int(self.sn_2) - int(self.sn_1)
            print(first_jump)
        except ValueError:
            print(f"{self.event} : {self.lifter}\n{self.list_t}")