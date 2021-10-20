#!/usr/bin/env python

import requests
import pandas
import csv
from bs4 import BeautifulSoup


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
                if len(td.text.strip()) > 0:
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
        table_headers = get_table_headers(result_table)
        table_rows = get_table_rows(result_table)
        table_rows.insert(0, table_headers)
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
        parsed_table = self.tier_check(table_rows)
        return parsed_table

    def get_event_result(self, event_id: int):
        event_page = self.BROWSER_SESSION.get(f"{self.EVENT_INDEX}&resource={event_id}")
        return self.strip_result_table(event_page.text)

    def main(self):
        with open("result_page.txt", 'r') as saved_file:
            result_page = saved_file.read()
        results = self.strip_result_table(result_page)
        self.data_analysis(results)

    def fetch_meets_by_year(self, year: int):
        """
        Probably going to make this a filtering function or something and
        dump the parsed index to a CSV type database
        """
        meet_options = self.strip_index_table()
        with open(f"meets_{year}.csv", "w") as csv_file:
            csvwrite = csv.writer(csv_file)
            csvwrite.writerow(meet_options[0])
            for meets in meet_options:
                if str(year) in meets[2]:
                    csvwrite.writerow(meets)

    def data_analysis(self, results_csv):
        """ OK so this bit is working """
        data = pandas.DataFrame(results_csv[1::], columns=results_csv[0:1:])
        print(data)


if __name__ == '__main__':
    scraper = DatabaseScraper()
    # scraper.strip_index_table()
    # scraper.main()
    scraper.fetch_meets_by_year(2021)
