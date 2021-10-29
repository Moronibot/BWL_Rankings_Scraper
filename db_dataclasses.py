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
    sn_2: str
    sn_3: str
    cj_1: str
    cj_2: str
    cj_3: str
    total: int
    sinclair: int
    expected_len: int = 14

    def __init__(self, db_line: list):
        if len(db_line) != self.expected_len:
            sys.exit(f"Entry not formatted correctly...\n{db_line}")
        self.bodyweight = db_line[5]
        self.sn_1 = db_line[6]
        self.sn_2 = db_line[7]
        self.sn_3 = db_line[8]
        self.cj_1 = db_line[9]
        self.cj_2 = db_line[10]
        self.cj_3 = db_line[11]

    def lift_increments(self):
        print(int(self.sn_1))
        if self.sn_1 is float:
            print(self.sn_1)
