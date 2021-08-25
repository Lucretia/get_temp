import sys
import time
import random
from calendar import month_name, month_abbr
from selenium import webdriver

if len(sys.argv) != 2:
    print("Usage: get_temp.py <place name>")

    sys.exit(1)

driver = webdriver.Chrome()
place = sys.argv[1]
url = "https://www.holiday-weather.com/"

def go_to(url):
    driver.get(url)

    time.sleep(random.randrange(1, 2))

    return (not is404() and hasData())

def is404():
    page_headers = driver.find_elements_by_tag_name('h1')

    for header in page_headers:
        if "404 Error" in header.text:
            return True;

    return False

def hasData():
    try:
        page_header = driver.find_element_by_xpath('//*[@id="maincontent"]/div/div[3]/div[2]/h1')
        header_text = page_header.get_attribute('innerText')

        if "No Averages Data Available" in header_text:
            return False
        else:
            return True
    except:
        # Element does not exist
        return False

if go_to(url + place + "/averages"):
    for month in range(2, 14):
        month_temp_in_c = driver.find_element_by_xpath(f'//*[@id="chart-head-temperature"]/div[3]/table/tbody/tr[2]/td[{month}]')
        print(f"{month_abbr[month - 1]} -> {month_temp_in_c.text} C")

driver.close()