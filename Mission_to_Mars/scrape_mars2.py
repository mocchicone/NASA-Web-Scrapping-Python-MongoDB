import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    mars["news_title"] = soup.find_all('div', class_='content_title')[1].get_text()
    mars["news_p"] = soup.find_all('div', class_='article_teaser_body')[0].get_text()

    print(mars)

    url3 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    baseurl = 'https://www.jpl.nasa.gov'
    browser.visit(url3)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')
    image = soup3.find_all('a', class_='button fancybox')[0].get('data-fancybox-href').strip()
    mars["featured_image_url"] = baseurl + image
    
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Description', 'Mars']
    df = df.set_index('Description')
    mars["html_table"] = df.to_html()

    url6 = "https://astrogeology.usgs.gov/"
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html5 = browser.html
    soup5 = bs(html5, "html.parser")
    images5 = soup5.find_all('div', class_='item')

    hemisphere_image_urls = []

    for x in images5:
         title = x.find('h3').text
         image_url2 = x.find('a', class_='itemLink product-item')['href']
         browser.visit(url6 + image_url2)
         html6 = browser.html
         soup6 = bs(html6, 'html.parser')
         img_url = url6 + soup6.find('img', class_='wide-image')['src']
         hemisphere_image_urls.append({'title': title, 'img_url' : img_url}) 

    mars["hemisphere_image_urls"] = hemisphere_image_urls
    

    browser.quit()

    return mars
    

