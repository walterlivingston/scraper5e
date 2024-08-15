from bs4 import BeautifulSoup

import scraper5e as s5

# Browser Setup
url = 'https://5etools.com/races.html'
driver = s5.start_driver(url)
s5.check_page_loaded(driver, url, 'lst__row ve-flex-col')

# Source Parsing
soup = BeautifulSoup(driver.page_source, 'html.parser')
races = soup.find_all('div', class_='lst__row ve-flex-col')

# Check for Data Files
# if os.path.exists("races.json"):
#     os.remove("races.json")

# Parsing of Race Data
for obj in races:
    sub_url = obj.find_all('a', href=True)[-1]['href']
    s5.check_page_loaded(driver, url+sub_url, 'lst__row ve-flex-col', 0)

    soup_race = BeautifulSoup(driver.page_source, 'html.parser')
    stats = soup_race.find('div', id="wrp-pagecontent")
    table = stats.find('table', id='pagecontent')
    tr = table.find_all('tr')
    for t in tr:
        # (TODO) Create logic for determining which segment is being processed
        # (TODO) Save to JSON
        name = t.find('h1', class_='stats-name copyable m-0')
        td = t.find('td')
        b = t.find('b')
        p = t.find('p')
        title = t.find('span', class_='entity-title-inner')
            
# Quit Browser
driver.quit()