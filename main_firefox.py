import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

options = webdriver.FirefoxOptions()

def set_driver_options(options:webdriver.FirefoxOptions):
    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36")
    options.set_preference("dom.webdriver.enabled", False)

set_driver_options(options)

caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "normal"

service = Service(executable_path=r"C:\WebDriver\geckodriver\geckodriver")
driver = webdriver.Firefox(service=service, options=options)

headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }

def click_ok(driver:webdriver.Firefox):
    try:
        el_ok = driver.find_element(By.XPATH, f"//a[contains(@id, 'cn-accept-cookie')]")
        el_ok.click()
    except NoSuchElementException:
        print(f"Кнопка ОК не найдена")
        pass     

def click_next(driver:webdriver.Firefox):
    el_plus = driver.find_element(By.XPATH, f"//a[contains(@class, 'paginate_button next')]")
    el_plus.click()

def get_pdf(el_download):
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
    with open(f"log.txt", "w") as file:
        file.write("")
    driver.get("https://cases.stretto.com/TuesdayMorning/claims/")
    time.sleep(1)
    click_ok(driver)
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
            print(f"z = {z} of {size_download}")
            get_pdf(els_downloads[z])
        time.sleep(1)
        with open("log.txt", "a") as file:
            file.write(f"Page {i} contains {size_download} files\n")

        click_next(driver)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()