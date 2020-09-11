#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pymongo

#Splinter example
import requests
import pandas as pd
import time

#Mongo Connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)



#Must have Chomedriver in folder
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[23]:


mars_url = 'https://mars.nasa.gov/news'
browser.visit(mars_url)
time.sleep(5)


# In[24]:



mars_html = browser.html
soup = bs(mars_html, "html.parser")


# In[25]:


#Navigate Mars latest article

news_date = soup.find("div", class_ = "list_date").text
print(news_date)
art_title = soup.find("div",class_ ="article_teaser_body").text
print(art_title)
art_teaser = soup.find("div", class_="content_title").text
print(art_teaser)


# # Mars Image

# In[26]:


#Navigate JPL featured image
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)
time.sleep(5)


# In[27]:


image_html = browser.html
soup = bs(image_html, 'html.parser')


# In[28]:


base_url = 'https://www.jpl.nasa.gov'

featured_image = soup.find(id='full_image')['data-fancybox-href']
#featured_image = soup.find(id='full_image').get('data-link')

featured_image=base_url + featured_image
#images = soup.find('img').get('image-src')
print(featured_image)


# # Mars Weather

# In[29]:


#attempting to get first tweet using bs
mars_weather  = 'https://twitter.com/marswxreport?lang=en'
browser.visit(mars_weather)
html = browser.html
soup = bs(html, "html.parser")

#mars_weather = soup.find('span class'="css-1dbjc4n", "tweet").text
#tweets = soup.find_all("li", attrs={"class":"js-stream-item"})


# In[31]:


mars_weather = (soup.find('div', attrs={"data-testid": "tweet"}).get_text()).split('InSight ')[1]

print(mars_weather)


# In[ ]:





# # Mars Facts- Diameter, Mass, etc.

# In[32]:


#using bs
mars_url = 'https://space-facts.com/mars/'
browser.visit(mars_url)
time.sleep(5)
mars_html = browser.html
soup = bs(mars_html, "html.parser")


# In[33]:


#Find and print all facts found for mars
facts1 = soup.find("tr",class_ = "row-1 odd").text
facts2 = soup.find("tr",class_ = "row-2 even").text
facts3 = soup.find("tr", class_="row-3 odd").text
facts4 = soup.find("tr", class_="row-4 even").text
facts5 = soup.find("tr", class_="row-5 odd").text
facts6 = soup.find("tr", class_="row-6 even").text
facts7 = soup.find("tr", class_="row-7 odd").text
facts8 = soup.find("tr", class_="row-8 even").text
facts9 = soup.find("tr", class_="row-9 odd").text


# In[34]:


#website through splinter module
mars_facts = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_facts)
#mars_facts.rows=["Description", "Value"]
mars_facts.columns=["Description", "Value"]
mars_facts.set_index("Description", inplace=True)
mars_facts


# In[35]:


#df to html
html = mars_facts.to_html()
print(html)


# # Mars Hemispheres 

# In[45]:


#website through splinter module
mars_hems_img ="https://astrogeology.usgs.gov"
mars_hems  = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(mars_hems)


# In[46]:


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
    

hem_img


# In[49]:


mars_data = {
    "news_date": news_date,
    "news_title": art_title,
    "news_p": art_teaser,
    "featured_image_url": featured_image,
    "mars_weather": mars_weather,
    "Fact Table": mars_facts,
    "hem_img": hem_img
}


# In[11]:


print(mars_data)


# In[50]:


get_ipython().system('jupyter nbconvert --to scrape_mars.py')


# In[ ]:





# In[ ]:




