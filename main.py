#!/usr/bin/env python
import time

start_time = time.time()

import requests
import csv
from bs4 import BeautifulSoup
from entry_dataclass import LiftEntry
from filtered_data.data_tools import dump_to_csv


def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers


def get_table_rows(table, data_id_res=False):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        tds = tr.find_all("td")
        if len(tds) == 0:
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            for td in tds:
                if data_id_res and len(td.find_all('i')) == 1:
                    strip_it = td.find_all('i')
                    cells.append(stripper(str(strip_it)))
                else:
                    cells.append(td.text.strip())
        rows.append(cells)
    return rows


def stripper(lazy_af: str):
    # fuck this shit, lets butcher this code.
    return lazy_af.split('data-id-resource="')[1].split('">')[0]


class DatabaseScraper:
    def __init__(self):
        self.BROWSER_SESSION = requests.Session()
        self.EVENT_INDEX = "https://bwl.sport80.com/event_results?id_ranking=8"
        self.RESULTS_DB: list = []

    def strip_result_table(self, page_text: str):
        result_table_id = "ranking-matches"
        soup = BeautifulSoup(page_text, "html.parser")
        result_table = soup.find("table", id=result_table_id)
        # table_headers = get_table_headers(result_table)
        table_rows = get_table_rows(result_table)
        # table_rows.insert(0, table_headers)
        return table_rows

    def tier_check(self, index_table):
        for meets in index_table[1::]:
            if meets[1] not in ['Tier 1', 'Tier 2', 'Tier 3', 'International']:
                meets.insert(1, "None")
        return index_table

    def strip_index_table(self):
        index_page = self.BROWSER_SESSION.get(self.EVENT_INDEX)
        result_table_id = "ranking-matches-resources"
        soup = BeautifulSoup(index_page.text, "html.parser")
        result_table = soup.find("table", id=result_table_id)
        table_headers = get_table_headers(result_table)
        table_rows = get_table_rows(result_table, True)
        table_rows.insert(0, table_headers)
        # Todo - make this shit modular...and the strip_results_table thing
        # parsed_table = self.tier_check(table_rows)
        parsed_table = table_rows
        return parsed_table

    def get_event_result(self, event_id: int):
        event_page = self.BROWSER_SESSION.get(f"{self.EVENT_INDEX}&resource={event_id}")
        return self.strip_result_table(event_page.text)

    def create_meets_index_db(self):
        """
        Will need to make an update version of this to stop pulling through all the shit again
        """
        meet_options = self.strip_index_table()
        with open(f"meets_index_db.csv", "w", newline='') as csv_file:
            csvwrite = csv.writer(csv_file)
            for meets in meet_options:
                csvwrite.writerow(meets)

    def create_results_db(self):
        event_id_list = []
        with open("meets_index_db.csv", "r") as index_file:
            index_csv = csv.reader(index_file)
            next(index_file)
            for rows in index_csv:
                event_id_list.append(int(rows[4]))
        for ids in event_id_list:
            self.write_results(ids)

    def write_results(self, event_id: int):
        with open("results_db.csv", "a", newline='') as results_db:
            csv_write = csv.writer(results_db)
            for rows in self.get_event_result(event_id):
                csv_write.writerow(rows)

    def check_results_db(self):
        """
        Runs through the results DB to make sure lines add up right
        """
        self.repeat_lifter: dict = {}
        with open("results_db.csv", "r") as index_file:
            index_csv = csv.reader(index_file)
            for rows in index_csv:
                self.repeat_lifter_count(rows)
        for lifters in self.repeat_lifter.values():
            print(lifters)

    def single_lifter_comps_one_year(self, year):
        self.repeat_lifter: dict = {}
        total_lifts_yr: int = 0
        with open("results_db.csv", "r") as index_file:
            index_csv = csv.reader(index_file)
            for rows in index_csv:
                if str(year) in rows[1]:
                    total_lifts_yr += 1
                    self.repeat_lifter_count(rows)
        self.repeat_lifter = dict(sorted(self.repeat_lifter.items(), key=lambda x: x[1], reverse=True))
        print(f"Lifter: Number of comps in {year}")
        comp_num = 6
        comp_log = 0
        for lifter, comp_n in self.repeat_lifter.items():
            if comp_n >= comp_num:
                print(f"{lifter}: {comp_n}")
                comp_log += 1
        print(f"Number of lifters with more than {comp_num} comps: {comp_log}")

    def filter_by_year(self, results_db: list, year: str) -> list:
        filtered_db = []
        for line in results_db:
            if year in line.date:
                filtered_db.append(line)
        return filtered_db

    def top_totals(self, year: str = None):
        results_db = self.load_results_db()
        if year:
            results_db = self.filter_by_year(results_db, year)
        top_lifts = {}
        for entry in results_db:
            if entry.lifter_name() not in top_lifts and entry.total_kg():
                top_lifts[entry.lifter_name()] = entry.total_kg()
            elif entry.lifter_name() in top_lifts and entry.total_kg() > top_lifts[entry.lifter_name()]:
                top_lifts[entry.lifter_name()] = entry.total_kg()

        sorted_lifts = (sorted(top_lifts.items(), key=lambda x: x[1], reverse=True))
        #return [(key, value) for key, value in top_lifts.items()]
        return sorted_lifts

    def load_results_db(self) -> list:
        results_db = []
        with open("results_db.csv", "r") as index_file:
            index_csv = csv.reader(index_file)
            for row in index_csv:
                results_db.append(LiftEntry(row))
        return results_db

    def repeat_lifter_count(self, csv_row: list):
        if csv_row[4].upper() not in self.repeat_lifter:
            self.repeat_lifter[csv_row[4].upper()] = 1
        elif csv_row[4].upper() in self.repeat_lifter:
            self.repeat_lifter[csv_row[4].upper()] += 1

    def check_index_db(self):
        """
        Runs through the results DB to make sure lines add up right
        """
        result_object = []
        with open("meets_index_db.csv", "r") as index_file:
            index_csv = csv.reader(index_file)
            for rows in index_csv:
                if len(rows) != 5:
                    print(rows)


if __name__ == '__main__':
    scraper = DatabaseScraper()
    # scraper.create_meets_index_db()
    # scraper.check_index_db()
    # scraper.create_results_db()
    # scraper.check_results_db()
    # scraper.single_lifter_comps_one_year(2021)
    # scraper.load_results_db()
    lifts = scraper.top_totals('2021')
    dump_to_csv("top_totals", lifts)

    print(f"--- {time.time() - start_time} seconds ---")
