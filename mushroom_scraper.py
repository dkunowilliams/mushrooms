from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
import os
import csv
import re


def get_images(query, driver):
    query_path = re.sub(r'\s+', '_', query)
    driver.get("https://www.google.com/")

    search = driver.find_element(By.NAME, 'q')
    search.send_keys(query, Keys.ENTER)
    elem = driver.find_element(By.LINK_TEXT, 'Images')
    elem.get_attribute('href')
    elem.click()
    sub = driver.find_elements(By.TAG_NAME, 'img')

    try:
        os.mkdir(query_path)
    except FileExistsError:
        pass

    j, failed_downloads = 0, 0
    for i in sub[3:]:
        src = i.get_attribute('src')
        try:
            if src != None:
                urllib.request.urlretrieve(str(src), os.path.join(
                    query_path, query_path + str(j) + '.png'))
                j += 1
            else:
                raise TypeError
        except TypeError:
            failed_downloads += 1

    print('Successful downloads:', j)
    print('Failed downloads:', failed_downloads, '\n')


def get_headers(filename):
    names = []
    with open(filename, mode='r') as f:
        csv_read = csv.reader(f, delimiter=',')
        for n, row in enumerate(csv_read):
            if not n:  # skip first row
                continue
            names.append(row[0])  # get names from first col
    return names


browser = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

names = get_headers('Mushroom_Dataset_Headers.csv')
for name in names:
    print('Getting images of class:', name)
    get_images(name.strip(), browser)
browser.close()
