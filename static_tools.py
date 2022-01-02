from magic_things import *


def strip_missed_lifts(recorded_lifts: list) -> list:
    made_lifts = []
    for n_lifts in recorded_lifts:
        if MISS_CHAR not in n_lifts and n_lifts != NO_LIFT_REC:
            made_lifts.append(int(n_lifts))
    return made_lifts


def label_lifts(lifts: list) -> list:
    labelled_lifts: list = []
    for n_lifts in lifts:
        if MISS_CHAR in n_lifts and n_lifts != NO_LIFT_REC:
            labelled_lifts.append((MISS, int(n_lifts.strip(MISS_CHAR))))
        elif n_lifts != NO_LIFT_REC:
            labelled_lifts.append((MADE, int(n_lifts.strip(MISS_CHAR))))
        elif n_lifts == NO_LIFT_REC:
            labelled_lifts.append((STR_NO_LIFT, BIG_NUM))
    if lift_order_correct(labelled_lifts):
        return labelled_lifts
    else:
        return sort_lift_order(labelled_lifts)


def made_lifts(lifts) -> list:
    return [lift for lift in lifts if lift.count(MADE)]


def lift_jump_percent(lift_a: int, lift_b: int) -> float:
    return round((lift_b - lift_a) / lift_a * N_MAX_PERCENT, 2)


def lift_order_correct(lifts: list):
    return True if lifts[0][1] <= lifts[1][1] <= lifts[2][1] else False


def sort_lift_order(lifts: list):
    lifts.sort(key=lambda x: x[1])
    return lifts


def best_lift(made_lifts: list):
    if len(made_lifts) != 0:
        return max(made_lifts)
    else:
        return 0


def distribute_data(float_list: list) -> dict:
    float_list_sorted = sorted(float_list, key=lambda x: float(x))
    lift_distributions = {}
    increment_step = (max(float_list) / (max(float_list) * 2))
    for x in range(int(max(float_list_sorted)) * 2):
        lower = x * increment_step
        upper = (x * increment_step) + increment_step
        lift_distributions[upper] = 0
        for i in float_list_sorted:
            if lower <= i <= upper:
                lift_distributions[upper] = lift_distributions[upper] + 1
    return lift_distributions


def convert_to_csv_list(dict_to_convert: dict) -> list:
    list_to_ret = []
    for x, y in dict_to_convert.items():
        list_to_ret.append([x, y])
    return list_to_ret


def split_date(date_str: str) -> tuple:
    year, month, day = map(int, date_str.split('-'))
    return day, month, year


def check_and_fix_entry(entry: list) -> list:
    for n in range(len(entry)):
        if len(entry[n]) == 0 and n <= 4:
            entry[n] = 'None'
        elif len(entry[n]) == 0 and n >= 5:
            entry[n] = NO_LIFT_REC
    return entry
