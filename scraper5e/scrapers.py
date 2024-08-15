from bs4 import BeautifulSoup
import json, os

from .browser import *

def scrape_races(filename:str='races.json'):
    # Check for Data Files
    if os.path.exists("races.json"):
        os.remove("races.json")

    # Browser Setup
    url = 'https://5etools.com/races.html'
    driver = start_driver(url)
    check_page_loaded(driver, url, 'lst__row ve-flex-col')

    # Source Parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    races = soup.find_all('div', class_='lst__row ve-flex-col')

    # Parsing of Race Data
    data = []
    for obj in races:
        sub_url = obj.find_all('a', href=True)[-1]['href']
        check_page_loaded(driver, (url + sub_url), 'lst__row ve-flex-col', 0)

        new_soup = BeautifulSoup(driver.page_source, 'html.parser')
        stats = new_soup.find('div', id="wrp-pagecontent")
        table = stats.find('table', id='pagecontent')
        tr = table.find_all('tr')
        race_dict = {}
        for item in tr:
            name = item.find('h1', class_='stats-name copyable m-0')
            td = item.find('td')
            b = item.find('b')
            more_flag = item.find('div', class_='rd__b rd__b--3') is not None

            if name is not None:
                race_dict['name'] = name.text
            if td is not None and b is not None:
                details = td.text.replace(b.text,'')
                race_dict[b.text] = details
            if more_flag:
                sub_data = item.find_all('div', class_='rd__b rd__b--3')
                for d in sub_data:
                    p = d.find('p')
                    attr_title = d.find('span', class_='entry-title-inner')
                    if p is not None and attr_title is not None:
                        race_dict[attr_title.text] = p.text

        data.append(race_dict)

    with open("races.json", "w") as f:
        json.dump(data, f)
                
    # Quit Browser
    driver.quit()