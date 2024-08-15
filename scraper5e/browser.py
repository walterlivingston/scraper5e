from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def start_driver(url: str):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-javascript")
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("network.http.use-cache", False)
    driver = webdriver.Firefox(options=options)
    driver.delete_all_cookies()
    driver.get(url)

    return driver

def check_page_loaded(driver, url:str, class_:str, wait_amt:int = 1, num_attempts:int = 5):
    pageNotLoaded= bool(True)
    attempts = 1
    while pageNotLoaded and attempts <= num_attempts:
        attempts += 1
        pageNotLoaded= False
        try:
            driver.get(url)
            driver.implicitly_wait(wait_amt)
        except TimeoutException:
            driver.quit()
            driver.implicitly_wait(wait_amt)
            driver.get(url)
            driver.implicitly_wait(wait_amt)

        try:
            driver.find_elements(By.CLASS_NAME, class_)
        except NoSuchElementException:
            pageNotLoaded = True
            
    if attempts > num_attempts:
        Warning('Did not load element within the number of attempts')