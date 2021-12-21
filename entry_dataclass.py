import dataclasses

N_TOTAL_LIFTS = 6
N_HALF_LIFTS = 3
N_MAX_PERCENT = 100
N_CUM_LIFT_PERCENT = N_MAX_PERCENT * 2

@dataclasses.dataclass
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
        self.lifter_name: str = entry_line[4].upper()
        self.bodyweight: float = float(entry_line[5])
        self.sn_1 = (entry_line[6])
        self.sn_2 = (entry_line[7])
        self.sn_3 = (entry_line[8])
        self.cj_1 = (entry_line[9])
        self.cj_2 = (entry_line[10])
        self.cj_3 = entry_line[11]
        self.total_kg: int = int(entry_line[12])
        self.sinclair = entry_line[13]
        self.full_entry = entry_line

    def made_snatches(self) -> tuple:
        snatches: list = [self.sn_1, self.sn_2, self.sn_3]
        made_snatches: list = []
        for n_snatch in snatches:
            if '-' not in n_snatch and n_snatch != '0':
                made_snatches.append(int(n_snatch))
        return int((len(made_snatches) / N_HALF_LIFTS) * 100), self.best_lift(made_snatches)

    def best_lift(self, made_lifts: list):
        if len(made_lifts) != 0:
            return max(made_lifts)
        else:
            return 0

    def made_cleanjerks(self) -> tuple:
        clean_jerks: list = [self.cj_1, self.cj_2, self.cj_3]
        made_clean_jerks: list = []
        for n_cleanjerk in clean_jerks:
            if '-' not in n_cleanjerk and n_cleanjerk != '0':
                made_clean_jerks.append(int(n_cleanjerk))
        return int((len(made_clean_jerks) / N_HALF_LIFTS) * 100), self.best_lift(made_clean_jerks)

    def overall_lift_percentage(self):
        return int(((self.made_snatches()[0] + self.made_cleanjerks()[0]) / N_CUM_LIFT_PERCENT) * N_MAX_PERCENT)