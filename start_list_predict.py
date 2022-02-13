""" Pull an events start list and compares all the lifters based upon current sinclair and total """
import requests
from main import DatabaseScraper
from filtered_data.data_tools import dump_to_csv


# https://bwl.sport80.com/public_reports/index/37918

def fetch_start_list(comp_id_num: int):
    browser = requests.Session()
    # resp = browser.get('https://bwl.sport80.com/events')
    # results = DatabaseScraper.strip_result_table(resp.text, table_id=None)
    start_list_page = browser.get(f"https://bwl.sport80.com/public_reports/index/{comp_id_num}")
    start_list = DatabaseScraper.strip_result_table(start_list_page.text, table_id=None)
    return start_list


def main():
    db_scrape = DatabaseScraper()
    start_list = fetch_start_list(37918)
    lifter_res = []
    for lifters in start_list:
        lifter_res.append(db_scrape.single_lifter_results(lifters[0].upper(), [2021, 2022]))
    dump_to_csv("crystal_palace", lifter_res)


if __name__ == '__main__':
    main()
