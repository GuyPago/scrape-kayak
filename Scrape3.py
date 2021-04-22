import csv
import selenium.webdriver.support.wait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import selenium.common.exceptions as selexcept
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
from random import randint, random
import os


def create_csv(data, dep_date, dep_country, arr_country):
    output_directory = './Output//' + dep_country + '-' + arr_country
    output_file = 'FlightData_' + dep_date[:6] + dep_date[8:] + '_' + dep_country + '-' + arr_country + '.csv'
    os.makedirs(os.path.dirname(output_directory), exist_ok=True)
    with open(output_directory + '//' + output_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(data)
        print(output_file + ' has been created')


def scroll_down(length=randint(650, 750)):
    for i in range(0, 1):
        browser.execute_script(f'window.scrollTo(0, {length});')
        time.sleep(0.1)
    return None


def close_ad():
    time.sleep(10)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()


def extract_page():
    time.sleep(randint(1, 2))
    page = browser.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')
    with open('html.txt', 'w', encoding='utf-8') as f:
        f.write(page)
    return page


def extract_data(data, dep_city, arr_country):
    soup_body = BeautifulSoup(data)

    div_flight_id = soup_body.findAll('div', {'class': 'dErF-carrier-text'})
    span_stops = soup_body.findAll('span', {'class': "stops-text"})
    span_price = soup_body.findAll('span', {'class': 'price-text'})
    span_duration = soup_body.findAll('span', {'class': 'dErF-leg-duration'})
    span_carrier = soup_body.findAll('span', {'class': 'codeshares-airline-names'})

    # flights_data = [['date', 'dep_country', 'arr_country', 'ticket_price_ILS', 'duration', 'carrier']]
    flights_data = []
    # Extracting data from tags

    for i in range(0, min(len(span_duration), len(span_carrier))):
        flights_data.append([date, span_carrier[i].text.strip(), dep_city, arr_country, span_stops[i].text.strip(),
                             span_duration[i].text.strip(), span_price[i].text.strip()[1:]])

    return flights_data


def scrape(scrape_date, arr_country, dep_country='TLV'):
    browser.get("https://www.il.kayak.com/flights")
    # browser.maximize_window()
    browser.implicitly_wait(6)

    search = browser.find_element(By.XPATH,
                                  "/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section["
                                  "2]/div/div/div[2]/form[1]/div[1]/div/div[2]/button")

    # choose one-way trip
    browser.find_element(By.XPATH,
                         "/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section[2]/div/div/div["
                         "1]/div[1]/div/div/div").click()
    browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/ul/li[2]').click()
    time.sleep(random())
    # choose and enter destination
    browser.find_element(By.XPATH,
                         '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section[2]/div/div/div['
                         '2]/form[1]/div[1]/div/div[1]/div/div[3]/div/div/div').click()
    time.sleep(0.1)
    choose_destination = browser.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div[1]/div[3]/input')
    choose_destination.send_keys(3*Keys.BACKSPACE + arr_country + Keys.RETURN)
    time.sleep(random())
    # choose and enter date (of the form dd.mm.yyyy)
    browser.find_element(By.XPATH,
                         '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section[2]/div/div/div['
                         '2]/form[1]/div[1]/div/div[1]/div/div[4]/div/div[1]/div').click()
    time.sleep(random() + 0.1)
    choose_date = browser.find_element(By.XPATH,
                                       '/html/body/div[6]/div/div[2]/div[1]/div[1]/div/div/div[1]/div[1]/div/div['
                                       '2]/div[1]')
    choose_date.send_keys(scrape_date)
    time.sleep(0.4)

    # Begin search
    search.click()
    close_ad()
    time.sleep(randint(5, 7))

    # Select no-stops only if possible, quit otherwise

    # try:
    #     browser.find_element(By.XPATH,
    #                          '/html/body/div[1]/div[1]/main/div/div[2]/div[2]/div/div[1]/div/div[3]/div/div[2]/div['
    #                          '1]/div[2]/div/div[3]/div[1]/li[1]/div/div[1]/div').click()
    # except Exception as e:
    #     return None
    # time.sleep(random()+2)

    scroll_down()
    # Scroll down and load more results
    for j in range(2):
        try:
            browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/a').click()
            scroll_down()
            time.sleep(random() + 3)
        except Exception as e:
            break
    scroll_down('document.body.scrollHeight')
    page = extract_page()
    flights = extract_data(page, dep_country, arr_country)
    create_csv(flights, scrape_date, dep_country, arr_country)


chromedriver_path = 'C:\\Users\\guypa\\Desktop\\Data\\Chromedriver.exe'

# 'VAR', 'TBS', 'BUS', 'TIA','SKG', 'RHO','HEL', 'ZAG', 'LON', 'NYC', 'AUH', 'BOJ', 'DXB', 'IEV',
destinations = ['TBS', 'PFO', 'LCA', 'IST', 'BAK']
dates = [str(i).zfill(2) + '.06.2021' for i in range(1, 31)]

for destination in destinations[:1]:
    # This will open a chrome window
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    browser = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_path)

    for date in dates:
        scrape(date, destination)
    browser.quit()
    print('done with', destination)
    time.sleep(5)


print('Closing chrome')

