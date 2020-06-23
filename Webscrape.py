# importing packages and modules
import bs4
from bs4 import BeautifulSoup as soup

# selenium helps with infinite page scrolling
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import time

import datetime

# restructure dates in python
date = datetime.datetime.today().strftime('%d-%b-%Y')

# website we will be scraping from
topman_url = 'https://us.topman.com/en/tmus/category/shoes-and-accessories-1928535/view-all-shoes-boots-5172704'

# defining the browser in our system to execute for scrape
binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
browser = webdriver.Firefox(firefox_binary=binary)

browser.get(topman_url)

# Scraping the text of "# results".
# We want to use this to create a condition(cond) that
# must be met in order to break our while loop and to
# further ensure that we are grabbing all shoes.
results = browser.page_source

results_soup = soup(results, "html.parser")

total_results = results_soup.find("span", {"class": "Filters-totalResults"})

cond = total_results.text
cond = str.split(cond)
cond = cond[0]
cond = int(cond)
# now that we have identified the value, parsed it and defined as integer
# we can set this as a condition to our infinite scrolling loop

# Infinite page scrolling to capture all the html.
# There was an issue with the page loading while
# scrolling to the bottom. For some reason sending
# scroll back up to the top and then back down again
# fixes this issue.
while True:
    browser.execute_script(
        "window.scrollTo(0, Math.max(document.body.offsetHeight));")
    time.sleep(3)
    browser.execute_script(
        "window.scrollTo(0, 0);")

    shoes = browser.page_source
    html_soup = soup(shoes, "html.parser")
    shoes = html_soup.findAll("div", {"class": "Product-meta"})
    if len(shoes) == cond:
        break

# displays the html tags of the first shoe
shoes[0]

# defining that tag to some variable
foot = shoes[0]

# creating title for csv file our data will go in
filename = "topmanshoes.csv"
# telling the file to open.
# Note: "w" will overwrite a file!
# Use "a" to append to an existing file.
f = open(filename, "a")

# creating the headers that will go inside our csv file
headers = "date, product_name, price, sale_price\n"
# writing the headers in our csv file
f.write(headers)

# looping each tag we want from entire html scrolled then writing it in csv
for foot in shoes:
    foot_name = foot.findAll("header", {"class": "Product-name"})
    product_name = foot_name[0].text
    foot_price = foot.findAll("span", {"class": "Price notranslate"})
    price = foot_price[0].text
    # some have sales some don't
    sale_price = foot_price[0].text
    if len(foot_price) == 2:
        sale_price = foot_price[1].text

    print("product_name: " + product_name)
    print("price: " + price)
    print("sale_price: " + sale_price)

    f.write(date + ',' + product_name + "," + price + "," + sale_price + "\n")

f.close()

# we now have a csv file with date, product name, price, and sale price
# of each Topman shoe :)
