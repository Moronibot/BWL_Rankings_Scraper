from dataclasses import dataclass


@dataclass
class LiftEntry:
    def __init__(self, entry_line: list):
        # ToDo - Move this to initial import of data
        for n in range(len(entry_line)):
            if len(entry_line[n]) == 0 and n <= 4:
                entry_line[n] = 'None'
            elif len(entry_line[n]) == 0 and n >= 5:
                entry_line[n] = '0'
        self.event: str = entry_line[0]
        self.date: str = entry_line[1]
        self.centre_ref: str = entry_line[2]
        self.lift_class: str = entry_line[3]
        self.lifter: str = entry_line[4].upper()
        self.bodyweight = (entry_line[5])
        self.sn_1 = (entry_line[6])
        self.sn_2 = (entry_line[7])
        self.sn_3 = (entry_line[8])
        self.cj_1 = (entry_line[9])
        self.cj_2 = (entry_line[10])
        self.cj_3 = (entry_line[11])
        self.total = entry_line[12]
        self.sinclair = entry_line[13]
        self.lift_attempts = [self.sn_1, self.sn_2, self.sn_3, self.cj_1, self.cj_2, self.cj_3]

    def date(self) -> str:
        return self.date

    def lifter_name(self) -> str:
        return self.lifter

    def top_snatch(self):
        pass

    def top_clean(self):
        pass

    def total_kg(self):
        return self.total

    def sinclair(self):
        return self.sinclair

    def lifter_bodyweight(self):
        pass

    def made_snatches(self):
        pass

    def made_cleanjerk(self):
        pass

    def made_lifts(self):
        pass
