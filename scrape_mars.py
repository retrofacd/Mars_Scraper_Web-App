#----------DEPENDENCIES-----------

from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()

#----------MARS NEWS--------------

    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url_1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    slide_elem = news_soup.find("div", class_="list_text")
    news_title = slide_elem.find("div", class_="content_title").text
    news_p = slide_elem.find("div", class_="article_teaser_body").text

    # mars_scrape["news_title"] = news_title
    # mars_scrape["news_p"] = news_p

#----------MARS IMAGE-----------

    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(5)

    browser.click_link_by_partial_text('more info')

    new_html = browser.html
    new_image_soup = BeautifulSoup(new_html, 'html.parser')

    img_url = new_image_soup.find("img", class_="main_image")
    img_url_2 = img_url.get("src")

    featured_image_url = "https://www.jpl.nasa.gov" + img_url_2

    # mars_scrape["featured_image_url"] = featured_image_url

#----------MARS WEATHER-----------

    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    weather_tweets = weather_soup.find_all("div", class_ = "js-tweet-text-container")

    for tweet in weather_tweets:
        if tweet.text.strip().startswith('Sol'):
            mars_weather = tweet.text.strip()

    # mars_scrape["mars_weather"] = mars_weather

#----------MARS FACTS-----------

    url_4 = 'http://space-facts.com/mars/'
    browser.visit(url_4)

    mars_data_read = pd.read_html(url_4)
    mars_data_df = pd.DataFrame(mars_data_read[0])
    mars_data_df.columns = ['Fact-ID','Fact-Value']
    mars_table_df = mars_data_df.set_index("Fact-ID")
    mars_table_html = mars_table_df.to_html(classes="mars_table_df")
    mars_table_html = mars_table_html.replace('\n',' ')

    # mars_scrape["mars_table_df"] = mars_table_html

#--------MARS HEMISPHERES-----------

    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_data=[]

    for i in range (4):
        time.sleep(10)
        images = browser.find_by_tag("h3")
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        image_title = soup.find("h2",class_="title").text
        image_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary = {"title":image_title,"img_url":image_url}
        hemisphere_data.append(dictionary)
        browser.back()

    # mars_scrape['hemisphere_data'] = hemisphere_data

#---------SUMMARY OF INFO-----------
    mars_scrape = {
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Table": mars_table_html,
        "Hemisphere_Data": hemisphere_data
    }

    return mars_scrape
