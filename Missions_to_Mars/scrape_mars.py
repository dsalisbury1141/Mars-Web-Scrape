#!/usr/bin/env python
# coding: utf-8
#Imports
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time



def init_browser():
#Must have Chomedriver in folder
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return Browser("chrome", **executable_path, headless=False)
############################################################################

def scrape():
    browser = init_browser()

    #Prepare to scrape Mars NASA
    mars_url = 'https://mars.nasa.gov/news'
    browser.visit(mars_url)
    time.sleep(5)

    #Browser informtion for scraping
    mars_html = browser.html
    soup = bs(mars_html, "html.parser")

    #Navigate Mars latest article
    news_date = soup.find("div", class_ = "list_date").text
    print(news_date)
    art_title = soup.find("div",class_ ="article_teaser_body").text
    print(art_title)
    art_teaser = soup.find("div", class_="content_title").text
    print(art_teaser)


    # # Mars Image

   
    #Prepare to scrape JPL featured image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(5)

    image_html = browser.html
    soup = bs(image_html, 'html.parser')


    #Navigate JPL featured image
    base_url = 'https://www.jpl.nasa.gov'

    featured_image = soup.find(id='full_image')['data-fancybox-href']
    #featured_image = soup.find(id='full_image').get('data-link')

    featured_image=base_url + featured_image
    #images = soup.find('img').get('image-src')
    print(featured_image)


        #Prepare to scrape and get first tweet using bs
    #mars_weather  = 'https://twitter.com/marswxreport?lang=en'
    #browser.visit(mars_weather)
    #html = browser.html
    #soup = bs(html, "html.parser")


      
    ##Prepare to scrape and get Mars Facts
    mars_url = 'https://space-facts.com/mars/'
    browser.visit(mars_url)
    time.sleep(5)
    mars_html = browser.html
    soup = bs(mars_html, "html.parser")

    
    #Same scrape using splinter module
    mars_facts = pd.read_html("https://space-facts.com/mars/")[0]
    print(mars_facts)
    #mars_facts.rows=["Description", "Value"]
    mars_facts.columns=["Description", "Value"]
    mars_facts.set_index("Description", inplace=True)
    mars_facts

    #Taking the marks facts to HTML
    mars_html = mars_facts.to_html()
    
    #Prepare to scrape astrogeology.usgs 
    mars_hems_img ="https://astrogeology.usgs.gov"
    mars_hems  = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_hems)

    # Create list and dictionary to collect Hemisphere data
    hem_img = []

    links = browser.find_by_tag("h3")

    for item in range(len(links)):
        hemisphere = {}
        
        # Find name
        browser.find_by_tag("h3")[item].click()
        
        # Get  Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Find Tag & Extract <href>
        sample_element = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Append to List
        hem_img.append(hemisphere)

    #print hemisphere data     
    hem_img

    
    #Collect all Mars Data into Dictionary
    mars_data = {
            "news_date": news_date,
            "news_title": art_title,
            "news_p": art_teaser,
            "featured_image_url": featured_image,
           # "mars_weather": mars_weather,
            "mars_facts": mars_html,
            "hem_img": hem_img
    }
    # In[11]:
    browser.quit()

    return mars_data













