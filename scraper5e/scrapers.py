from bs4 import BeautifulSoup
import json, os

from .browser import *

def start_scrape(scraping:str, class_:str, path:str=''):
    # Check for Data Files
    if path and not os.path.exists(path):
        os.mkdir(path)

    if os.path.exists(path+scraping+'.json'):
        os.remove(path+scraping+'.json')

    # Browser Setup
    url = 'https://5etools.com/'+scraping+'.html'
    driver = start_driver(url)
    check_page_loaded(driver, url, class_)

    return driver, url

def scrape_classes(path:str = ''):
    # Start Scraping
    driver, url = start_scrape('classes', 'list list--stats classes cls__list', path)

    # Source Parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    classes = soup.find_all('li', class_='lst__row ve-flex-col')

    # Parsing of Class Data
    data = []
    for obj in classes:
        class_dict = {}
        new_soup = BeautifulSoup(driver.page_source, 'html.parser')
        stats = new_soup.find('div', id='statsprof')
        name = stats.find('div', class_='cls-side__name')
        class_dict['name'] = name.text

        tr = stats.find_all('tr')
        for item in tr:
            sect = item.find('h5', class_='cls-side__section-head')
            null_div = item.find_all('div', class_='')
            if sect is not None:
                class_dict[sect.text] = {}
                for div in null_div:
                    b = div.find('b')
                    st = div.find('strong')
                    p = div.find('p')
                    # Multiclassing
                    if b is not None and p is not None:
                        mc_reqs = item.find('div', class_='cls-side__mc-prof-intro--requirements')
                        details = div.text.replace(b.text,'')
                        class_dict[sect.text][b.text] = details
                        if mc_reqs is not None:
                            class_dict[sect.text]['Requirements:'] = mc_reqs.text
                            
                    # Proficiencies
                    elif b is not None:
                        details = div.text.replace(b.text,'')
                        class_dict[sect.text][b.text] = details
                    # Hit Points
                    elif st is not None:
                        details = div.text.replace(st.text,'')
                        class_dict[sect.text][st.text] = details
                    # Starting Equipment
                    else:
                        eqmt = div.find_all('li')
                        e_vals = []
                        for e in eqmt:
                            e_vals.append(e.text)
                        gp = div.find('span', {'title':'Starting Gold. Click to roll. SHIFT/CTRL to roll twice.'})
                        class_dict[sect.text]['Equipment:'] = e_vals
                        class_dict[sect.text]['Alternate:'] = gp.text + 'gp'
        
        # Parse Level Table
        level_tbl = new_soup.find('table', class_='cls-tbl shadow-big w-100 mb-2')
        tr = level_tbl.find_all('tr', class_='')
        th = tr[-2].find_all('th')
        columns = []
        for item in th:
            columns.append(item.text)
        columns = columns[1:]
        levels = level_tbl.find_all('tr', class_='cls-tbl__stripe-odd')
        class_dict['Levels'] = {}
        for item in levels:
            level = item.find('td', class_='cls-tbl__col-level')
            class_dict['Levels'][level.text] = {}
            vals = item.find_all('td')
            vals = vals[1:]
            for i, val in enumerate(vals):
                class_dict['Levels'][level.text][columns[i]] = val.text

        data.append(class_dict)
        
        sub_url = obj.find_all('a', href=True)[-1]['href']
        check_page_loaded(driver, (url + sub_url), 'lst__row ve-flex-col', 0)

    with open(path+'classes.json', "w") as f:
        json.dump(data, f)

    driver.quit()

def scrape_races(path:str=''):
    # Start Scraping
    driver, url = start_scrape('races', 'lst__row ve-flex-col', path)

    # Source Parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    races = soup.find_all('div', class_='lst__row ve-flex-col')

    # Parsing of Race Data
    data = []
    for obj in races:
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

            # Race Name
            if name is not None:
                race_dict['name'] = name.text
            # Core Details
            if td is not None and b is not None:
                details = td.text.replace(b.text,'')
                race_dict[b.text] = details
            # Other Details
            if more_flag:
                sub_data = item.find_all('div', class_='rd__b rd__b--3')
                for d in sub_data:
                    p = d.find('p')
                    attr_title = d.find('span', class_='entry-title-inner')
                    if p is not None and attr_title is not None:
                        race_dict[attr_title.text] = p.text

        data.append(race_dict)
        
        sub_url = obj.find_all('a', href=True)[-1]['href']
        check_page_loaded(driver, (url + sub_url), 'lst__row ve-flex-col', 0)

    with open(path+'races.json', "w") as f:
        json.dump(data, f)
                
    # Quit Browser
    driver.quit()