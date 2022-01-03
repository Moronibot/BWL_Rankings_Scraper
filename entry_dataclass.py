import dataclasses
from static_tools import *
from magic_things import *


@dataclasses.dataclass
class LiftEntry:
    def __init__(self, entry_line: list):
        self.event: str = entry_line[0]
        self.day, self.month, self.year = split_date(entry_line[1])
        self.centre_ref: str = entry_line[2]
        self.lift_class: str = entry_line[3]
        self.lifter_name: str = entry_line[4].upper()
        self.bodyweight: float = float(entry_line[5])
        self.snatches: list = [entry_line[6], entry_line[7], entry_line[8]]
        self.clean_jerks: list = [entry_line[9], entry_line[10], entry_line[11]]
        self.total_kg: int = int(entry_line[12])
        self.sinclair: int = int(entry_line[13])
        self.full_entry: list = entry_line
        self.lifter_gender: str = gender(entry_line[3])

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
