{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import time\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as bs\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "\n",
    "def init_browser():\n",
    "    \n",
    "    executable_path = {\"executable_path\": \"chromedriver\"}\n",
    "    return Browser(\"chrome\", **executable_path, headless=False)\n",
    "\n",
    "def scrape():\n",
    "    browser = init_browser()\n",
    "    mars = {}\n",
    "\n",
    "    url = \"https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest\"\n",
    "    browser.visit(url)\n",
    "    time.sleep(1)\n",
    "    html = browser.html\n",
    "    soup = bs(html, \"html.parser\")\n",
    "\n",
    "    mars[\"news_title\"] = soup.find_all('div', class_='content_title')[1].get_text()\n",
    "    mars[\"news_p\"] = soup.find_all('div', class_='article_teaser_body')[1].get_text()\n",
    "\n",
    "    url3 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "    browser.visit(url3)\n",
    "    html3 = browser.html\n",
    "    soup3 = bs(html3, 'html.parser')\n",
    "    image = soup3.find_all('a', class_='button fancybox')[0].get('data-fancybox-href').strip()\n",
    "    mars[\"featured_image_url\"] = url3 + image\n",
    "    \n",
    "    url4 = 'https://space-facts.com/mars/'\n",
    "    tables = pd.read_html(url4)\n",
    "    df = tables[0]\n",
    "    df.columns = ['Description', 'Mars']\n",
    "    mars[\"html_table\"] = df.to_html()\n",
    "\n",
    "    url6 = \"https://astrogeology.usgs.gov/\"\n",
    "    url5 = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "    browser.visit(url5)\n",
    "    html5 = browser.html\n",
    "    soup5 = bs(html5, \"html.parser\")\n",
    "    images5 = soup5.find_all('div', class_='item')\n",
    "\n",
    "    mars[\"hemisphere_image_urls\"] = []\n",
    "\n",
    "    for x in images5:\n",
    "        title = x.find('h3').text\n",
    "        image_url2 = x.find('a', class_='itemLink product-item')['href']\n",
    "        browser.visit(url6 + image_url2)\n",
    "        html6 = browser.html\n",
    "        soup6 = bs(html6, 'html.parser')\n",
    "        img_url = url6 + soup6.find('img', class_='wide-image')['src']\n",
    "        hemisphere_image_urls.append({'title': title, 'img_url' : img_url}) \n",
    "    \n",
    "    return mars\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
