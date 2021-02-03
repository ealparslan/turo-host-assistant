from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

import datetime, time, re, csv, sys

import config

RE_REMOVE_HTML = re.compile('<.+?>')

SLEEP_SECONDS = 3

class TuroHostAssistant:
    def __init__(self):
        self.driver = webdriver.Chrome(config.driverLocation) 
        self.driver.set_page_load_timeout(30)

    def assist(self, outfile):
        self.login()
        time.sleep(SLEEP_SECONDS)
        trips = self.get_trips()
        self.write(trips, outfile)
        self.stop()

    def login(self):
        self.driver.get('https://turo.com/login')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div/div/div/div[1]/div/iframe")))
        iframe = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div/div/div[1]/div/iframe")
        self.driver.switch_to.frame(iframe)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='email']"))).send_keys(config.TURO_USERNAME)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(config.TURO_PASSWORD)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/form/button"))).click()

    def write(self, rows, out):
        print 'Writing to out file', out
        rows = [x for x in rows if x != None]
        with open(out, 'w') as f:
            w = csv.DictWriter(f,fieldnames = config.fieldnames, delimiter=',')
            w.writeheader()
            w.writerows(rows)

    def stop(self):
        self.driver.close()

    def get_datetime(self, raw_string):
        # Remove the header text
        cleaned_str = re.sub('.*\n', '', 
                raw_string, count = 1)

        return datetime.datetime.strptime(cleaned_str, '%a, %b %d, %Y\n%I:%M %p')

    def get_trip(self, reservation_url):
        print 'Getting trip', reservation_url

        self.driver.get(reservation_url + '/receipt/')

        anyerror = self.driver.find_elements(By.CLASS_NAME, 'error-page')
        if anyerror:
            return {}


        pickup, dropoff = [self.get_datetime(x.text) for x in self.driver.find_elements_by_class_name('receiptSchedule')]

        line_items = self.driver.find_elements_by_class_name('line-item')

        results = {'URL': reservation_url,
                'PICKUP': pickup,
                'DROPOFF': dropoff}
        for item in line_items:
            name = item.find_element_by_class_name('label').text
            if name == 'YOU PAID': # Ignore trips where I didn't host
                return None
            value = item.find_element_by_class_name('value').text
            if name != 'GUEST':
                value = float(re.search('[\d|\.]+', value).group())

            if 'additional miles' in name.lower():
                name = 'ADDITIONAL MILES DRIVEN'
            elif 'tolls' in name.lower():
                name = 'TOLLS'
            elif 'total miles' in name.lower():
                name = 'TOTAL MILES'
            elif 'cleaning' in name.lower():
                name = 'CLEANING'
            elif 'discount' in name.lower():
                name = 'DISCOUNT'
            elif 'gas' in name.lower():
                name = 'GAS'
            elif 'smoking' in name.lower():
                name = 'SMOKING'

            results[name] = value

        return results


    def get_trips(self, page_slug = None):

        with open('trips.txt') as f:
            all_trips = f.readlines()
        trip_links = set(all_trips)


        print 'Trip Links', trip_links

        trip_details = [self.get_trip(trip_link) for trip_link in trip_links]

        print trip_details

        return trip_details

if __name__ == '__main__':
    outfile = 'output.csv'
    if len(sys.argv) > 1:
        outfile = sys.argv[1]

    assistant = TuroHostAssistant()
    assistant.assist(outfile)
