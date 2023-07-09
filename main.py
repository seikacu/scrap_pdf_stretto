import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()

def set_driver_options(options:webdriver.ChromeOptions):
    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36")

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    options.debugger_address = 'localhost:8989'


set_driver_options(options)

caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'eager'

service = Service(desired_capabilities=caps, executable_path=r"C:\WebDriver\chromedriver\chromedriver.exe") # desired_capabilities=caps,
driver = webdriver.Chrome(service=service, options=options)

headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }

def click_next(driver:webdriver.Chrome):
    el_plus = driver.find_element(By.XPATH, f"//a[contains(@class, 'paginate_button next')]")
    el_plus.click()

def get_pdf(driver:webdriver.Chrome, el_download):
    try:
        url_link = el_download.get_attribute('href')
        if len(url_link) > 0:
            start_index = url_link.rfind('/') + 1
            end_index = url_link.rfind('.')
            name = url_link[start_index:end_index]
                    
            req = requests.get(url=url_link, headers=headers)
            response = req.content
            with open(f"pdf/{name}.pdf", "wb") as file:
                file.write(response)
        else:
             print(f"Ссылка на PDF файл не найдена")
    except NoSuchElementException:
        print(f"Ссылка на PDF файл не найдена")
        pass

try:
    driver.get("https://cases.stretto.com/TuesdayMorning/claims/")
    time.sleep(3)
    for i in range(1, 188):
        print(f"i = {i}")
        time.sleep(3)
        els_plus = driver.find_elements(By.XPATH, f"//div[contains(@class, 'hide-show-table-row')]")
        time.sleep(3)
        size_plus = els_plus.__len__()
        for j in range(0, size_plus):
            els_plus[j].click()
            print(f"i = {i}, j = {j}")
            time.sleep(1)
            
        time.sleep(1)
        els_downloads = driver.find_elements(By.CSS_SELECTOR, '.creditor-detail-box a')
        size_download = els_downloads.__len__()
        for z in range(0, size_download):
            print(f"z = {z}")
            get_pdf(driver, els_downloads[z])
        time.sleep(1)
        click_next(driver)
except Exception as ex:
    print(ex)