#!/usr/bin/env python

import time

start_time = time.time()

import requests
import csv
from bs4 import BeautifulSoup
from db_dataclasses import LifterResult


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
        #parsed_table = self.tier_check(table_rows)
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
        with open("results_db.csv", "r") as index_file:
            index_csv = csv.reader(index_file)
            for rows in index_csv:
                if str(year) in rows[1]:
                    self.repeat_lifter_count(rows)
        self.repeat_lifter = dict(sorted(self.repeat_lifter.items(), key=lambda x: x[1], reverse=True))
        print(f"Lifter: Number of comps in {year}")
        for lifter, comp_n in self.repeat_lifter.items():
            print(f"{lifter}: {comp_n}")

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
    #scraper.create_meets_index_db()
    #scraper.check_index_db()
    #scraper.create_results_db()
    #scraper.check_results_db()
    scraper.single_lifter_comps_one_year(2021)

    print(f"--- {time.time() - start_time} seconds ---")
