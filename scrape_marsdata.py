
# coding: utf-8

# In[1]:


# # Import Libraries
# from splinter import Browser
# from bs4 import BeautifulSoup as bs
# import requests as r
# import pprint
# import pandas as pd
# import time
# import re


# In[2]:


#path to chromedriver (to find path)

# get_ipython().system('which chromedriver ')


# # NASA Mars News

# In[3]:


# Initialize Browser



# In[4]:
def scrape():
    print("COMMENCING SCRAPE")
    print("----------------------------------")
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import requests as r
    import pprint
    import pandas as pd
    import time
    import re

# creating an empty dict to all all data
    mars_dict= {}

    executable_path= {"executable_path":"/usr/local/bin/chromedriver"}
    browser= Browser("chrome", **executable_path, headless= False)

    #Visit the Nasa Web for Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    #Scrape page into soup
    html = browser.html
    soup= bs(html,"html.parser")

    # find news title and Paragraph

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_ ="article_teaser_body").text
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p


    # In[5]:


    #test variables
    print(news_title)
    print(news_p)


    # # JPL Mars Space Images - Featured Image

    # In[6]:


    # setting up the URL for the feature image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)


    # In[7]:


    # find and click the image info
    feature_img_elem = browser.find_by_id('full_image')
    feature_img_elem.click()


    # In[8]:


    browser.is_element_present_by_text("more info", wait_time =1)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()


    # In[9]:


    html= browser.html
    image_soup= bs(html,"html.parser")


    # In[10]:


    img_url_rel = image_soup.select_one('figure.lede a img').get("src")


    # In[11]:


    print(img_url_rel)


    # In[12]:


    feature_img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    mars_dict["feature_img_url"]=feature_img_url

    # In[13]:


    print(feature_img_url)


    # # Mars Weather

    # In[14]:


    # setting up the URL and browser
    Mars_tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(Mars_tweet_url)


    # In[15]:


    # config the html to get news (scrape page into soup)
    mars_weather_html = browser.html
    mars_weather_soup= bs(mars_weather_html,"html.parser")


    # In[16]:


    tweet= mars_weather_soup.find("div", class_= "js-tweet-text-container")


    # In[17]:


    mars_weather= tweet.get_text()
    print(mars_weather)
    mars_dict["mars_weather"]= mars_weather

    # ## Mars Facts

    # In[18]:

    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    # mars_facts_data["mars_facts_table"] = mars_html_table
    mars_dict["mars_facts"]=mars_html_table
    mars_html_table
    # ## Mars Hemispheres

    # In[9]:


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

    #     print(hemi_dicts)

    # In[18]:

    print('-----------------------------------------------')
    print(mars_dict)
    return mars_dict
# Scrape()
