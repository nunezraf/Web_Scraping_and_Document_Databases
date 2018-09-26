# import Libraries
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pprint
import requests as r
import pandas as pd
import time
import tweepy
import pymongo
#----------------------------------------------------------------
# NASA Mars News
#Scrape Function
def init_browser():
    executable_path = {'executable_path': './chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def Scrape():
    print("COMMENCING SCRAPE")
    print("----------------------------------")

    #empty Dictionary
    browser = init_browser()
    mars_dict= {}


    #--------------------------------------
    #NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #Scrape page into soup
    html = browser.html
    soup= bs(html,"html.parser")

    # find news title and Paragraph

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_ ="article_teaser_body").text

    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p

    print("NEWS TITLE & DESCRIPTION ACQUIRED")

#------------------------------------------------
#JPL Mars space Images - Featured Image
#--------------------------------------------------------------------
#   # setting up the URL for the feature image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


    #Setting up Splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', executable_path = "chromedriver", headless=True)

    browser.visit(url)
#
#     # find and click the image info
    feature_img_elem = browser.find_by_id('full_image')
    feature_img_elem.click()
#
    browser.is_element_present_by_text("more info", wait_time =1)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()
#
    html= browser.html
    image_soup= bs(html,"html.parser")
#
    img_url_rel = image_soup.select_one('figure.lede a img').get("src")
#
    feature_img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    mars_dict["feature_img_url"]=feature_img_url

    print("FEATURED IMAGE ACQUIRED")
# #-------------------------------------------------------------------------
# Mars Weather
# def mars_weather():

    executable_path= {"executable_path":"/usr/local/bin/chromedriver"}
    browser= Browser("chrome", executable_path = "chromedriver" , headless= True)

    # setting up the URL and browser
    Mars_tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(Mars_tweet_url)

    # config the html to get news (scrape page into soup)
    mars_weather_html = browser.html
    mars_weather_soup= bs(mars_weather_html,"html.parser")

    tweet= mars_weather_soup.find("div", class_= "js-tweet-text-container")

    mars_weather= tweet.get_text()

    mars_dict["mars_weather"]= mars_weather
    print("WEATHER ACQUIRED")

# #-----------------------------------------------------------------------
# # Mars Facts
# # visit space facts and scrap the mars facts table

    executable_path= {"executable_path":"/usr/local/bin/chromedriver"}
    browser= Browser("chrome", executable_path = "chromedriver" , headless= True)

    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    time.sleep(1)
    mars_facts_html = browser.html
    mars_facts_soup = bs(mars_facts_html, 'html.parser')

    fact_table = mars_facts_soup.find('table', class_='tablepress tablepress-id-mars')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    facets = []
    values = []

    for row in column1:
        facet = row.text.strip()
        facets.append(facet)

    for row in column2:
        value = row.text.strip()
        values.append(value)

        mars_facts = pd.DataFrame({
            "Facet":facets,
            "Value":values
            })

        mars_facts_html = mars_facts.to_html(header=False, index=False)

        mars_dict['mars_facts'] = mars_facts

        print("FACTS ACQUIRED")


    # Mars Hemispheres---------------------------------

    # Mars Hemispheres URL
    # url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #
    # # Empty list of image urls
    # hemisphere_image_urls = []
    #
    #
    # # ### Valles Marineris
    #
    # # Setting up splinter
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', executable_path = "chromedriver", headless=True)
    #
    # browser.visit(url)
    #
    # # Moving through pages
    # time.sleep(5)
    # browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    # time.sleep(5)
    #
    # # Create BeautifulSoup object; parse with 'html.parser'
    # html = browser.html
    # soup = bs(html, 'html.parser')
    #
    # # Store link
    # valles_link = soup.find('div', 'downloads').a['href']
    #
    # # Create dictionary
    # valles_marineris = {
    #     "title": "Valles Marineris Hemisphere",
    #     "img_url": valles_link
    # }
    #
    # # Appending dictionary
    # hemisphere_image_urls.append(valles_marineris)
    #
    #
    # # ### Cerberus
    #
    # # Setting up splinter
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', executable_path = "chromedriver", headless=True)
    #
    # browser.visit(url)
    #
    # # Moving through pages
    # time.sleep(5)
    # browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    # time.sleep(5)
    #
    # # Create BeautifulSoup object; parse with 'html.parser'
    # html = browser.html
    # soup = bs(html, 'html.parser')
    #
    # # Store link
    # cerberus_link = soup.find('div', 'downloads').a['href']
    #
    # # Create dictionary
    # cerberus = {
    #     "title": "Cerberus Hemisphere",
    #     "img_url": cerberus_link
    # }
    #
    # # Appending dictionary
    # hemisphere_image_urls.append(cerberus)
    #
    #
    # # ### Schiaparelli
    #
    # # Setting up splinter
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', executable_path = "chromedriver", headless=True)
    #
    # browser.visit(url)
    #
    # # Moving through pages
    # time.sleep(5)
    # browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    # time.sleep(5)
    #
    # # Create BeautifulSoup object; parse with 'html.parser'
    # html = browser.html
    # soup = bs(html, 'html.parser')
    #
    # # Store link
    # schiaparelli_link = soup.find('div', 'downloads').a['href']
    #
    # # Create dictionary
    # schiaparelli = {
    #     "title": "Schiaparelli Hemisphere",
    #     "img_url": schiaparelli_link
    # }
    #
    # # Appending dictionary
    # hemisphere_image_urls.append(schiaparelli)
    #
    #
    # # ### Syrtis Major
    #
    # # Setting up splinter
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', executable_path = "chromedriver", headless=True)
    #
    # browser.visit(url)
    #
    # # Moving through pages
    # time.sleep(5)
    # browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    # time.sleep(5)
    #
    # # Create BeautifulSoup object; parse with 'html.parser'
    # html = browser.html
    # soup = bs(html, 'html.parser')
    #
    # # Store link
    # syrtis_link = soup.find('div', 'downloads').a['href']
    #
    # # Create dictionary
    # syrtis_major = {
    #     "title": "Syrtis Major Hemisphere",
    #     "img_url": syrtis_link
    # }
    #
    # # Appending dictionary
    # hemisphere_image_urls.append(syrtis_major)
    #
    # # Adding to dictionary
    # mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

#-------------------------------------------

    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for x in range(1,9,2):
        hemi_dict = {}

        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = bs(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[x].text.strip('Enhanced')

        detail_links = browser.find_by_css('a.product-item')
        detail_links[x].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()

        hemi_img_soup = bs(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        print(hemi_name)
        hemi_dict['title'] = hemi_name.strip()

        print(hemi_img_path)
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

        mars_dict["hemisphere_imgs"]= hemi_dicts


#-------------------------------------------

    print("HEMISPHERE IMAGES ACQUIRED")
    print("----------------------------------")
    print("SCRAPING COMPLETED")

    return mars_dict
# Scrape()
