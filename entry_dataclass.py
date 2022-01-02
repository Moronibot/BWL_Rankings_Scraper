import dataclasses
from static_tools import *
from magic_things import *


@dataclasses.dataclass
class LiftEntry:
    def __init__(self, entry_line: list):
        # ToDo - Move this to initial import of data
        for n in range(len(entry_line)):
            if len(entry_line[n]) == 0 and n <= 4:
                entry_line[n] = 'None'
            elif len(entry_line[n]) == 0 and n >= 5:
                entry_line[n] = NO_LIFT_REC
        self.event: str = entry_line[0]
        self.date: str = entry_line[1]
        self.centre_ref: str = entry_line[2]
        self.lift_class: str = entry_line[3]
        self.lifter_name: str = entry_line[4].upper()
        self.bodyweight: float = float(entry_line[5])
        self.sn_1 = (entry_line[6])
        self.sn_2 = (entry_line[7])
        self.sn_3 = (entry_line[8])
        self.snatches: list = [self.sn_1, self.sn_2, self.sn_3]
        self.cj_1 = (entry_line[9])
        self.cj_2 = (entry_line[10])
        self.cj_3 = entry_line[11]
        self.clean_jerks: list = [self.cj_1, self.cj_2, self.cj_3]
        self.total_kg: int = int(entry_line[12])
        self.sinclair = int(entry_line[13])
        self.full_entry = entry_line

    def made_snatches(self) -> tuple:
        made_snatches: list = strip_missed_lifts(self.snatches)
        return int((len(made_snatches) / N_HALF_LIFTS) * N_MAX_PERCENT), best_lift(made_snatches)

    def made_cleanjerks(self) -> tuple:
        made_clean_jerks: list = strip_missed_lifts(self.clean_jerks)
        return int((len(made_clean_jerks) / N_HALF_LIFTS) * N_MAX_PERCENT), best_lift(made_clean_jerks)

    def overall_lift_percentage(self):
        return int(((self.made_snatches()[0] + self.made_cleanjerks()[0]) / N_CUM_LIFT_PERCENT) * N_MAX_PERCENT)

    def first_snatch_jump(self) -> tuple:
        first, second, third = label_lifts(self.snatches)
        jump_succ_weight: tuple = ()
        if first[0] == MADE == second[0]:
            jump_succ_weight = (MADE, (lift_jump_percent(first[1], second[1])))
        return jump_succ_weight

    def second_snatch_jump(self) -> tuple:
        first, second, third = label_lifts(self.snatches)
        jump_succ_weight: tuple = ()
        if second[0] == MADE == third[0]:
            jump_succ_weight = (MADE, (lift_jump_percent(second[1], third[1])))
        return jump_succ_weight

    def first_cj_jump(self) -> tuple:
        first, second, third = label_lifts(self.clean_jerks)
        jump_succ_weight: tuple = ()
        if first[0] == MADE == second[0]:
            jump_succ_weight = (MADE, (lift_jump_percent(first[1], second[1])))
        return jump_succ_weight

    def second_cj_jump(self) -> tuple:
        first, second, third = label_lifts(self.clean_jerks)
        jump_succ_weight: tuple = ()
        if second[0] == MADE == third[0]:
            jump_succ_weight = (MADE, (lift_jump_percent(second[1], third[1])))
        return jump_succ_weight
