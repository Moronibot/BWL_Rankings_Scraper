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