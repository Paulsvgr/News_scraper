from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import string
import requests
import re
from db import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class Scrape(Database):
    def __init__(self) -> None:
        super().__init__()
        self.stop_words = set(stopwords.words('english'))
        self.webbsite_dic = {
                            "Bbc": self.scrape_bbc,
                            "Apnews": self.scrape_appnews, 
                            "Huffpost": self.scrape_huffpost
                            }
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'referrer': 'https://google.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Pragma': 'no-cache'}

    def go(self):
        self.date_list, self.check = self.add_current_date()
        if self.check:
            self.websites_lists = self.get_all_websites()
            if self.check_if_same_day():
                self.scrape_webbsites()
        else:
            return "Already scraped todad\n"
        return f"Scraping for today just finished {self.date_list[0]}\n"

    def get_response(self, url):
        try:
            response = requests.get(url, headers=self.headers)
        except requests.exceptions.RequestException:
            print(f"Couldn't get any response from {url}")
        else:
            # Check that the request was successful
            if response.status_code == 200:
                
                # Create a BeautifulSoup object from the response content
                soup = BeautifulSoup(response.content, "html.parser")
                return soup

    def scrape_webbsites(self):
        ###
        for website_str, website, website_url in self.websites_lists:
            self.webbsite = website
            self.webbsite_url = website_url
            if website_str in self.webbsite_dic.keys():
                self.webbsite_dic[website_str]()
            else:
                self.scrape_other_website()

    def check_if_same_day(self):
        dates_lists = self.get_dates()
        for date_list in dates_lists:
            if date_list[0] == datetime.today().date():
                return False
        return True

    def text_to_words(self, text):
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Tokenize the text into words
        words = word_tokenize(text)

        # Remove stopwords and create a frequency dictionary
        word_freq = {}
        for word in words:
            if word.lower() not in self.stop_words:
                if word not in word_freq:
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

        return word_freq


    def scrap_url_huffpost(self, url):
        soup = self.get_response(url)
        article_text = ""
        texts = soup.find_all("div",{"class":"primary-cli cli cli-text"})
        for text in texts:
            article_text += text.text+ "\n"
        return article_text

    def scrape_huffpost(self):
        page_nb = 1
        next_page = True

        while next_page:
            soup = self.get_response(f"https://www.huffpost.com/news/?page={page_nb}")
            articles = soup.find_all("a",{"class":"card__headline card__headline--long"})
            for article in articles:
                url = article["href"]
                url_id, check = self.add_url(url, self.webbsite)
                if check:
                    text = self.scrap_url_huffpost(url)
                    if text:
                        words_freq = self.text_to_words(text)
                        self.add_words_to_url(words_freq, url_id)
                self.add_date_to_url(self.date_list[1], url_id)
            print(f"                     -----------------{page_nb}--------------")
            page_nb += 1
            nexts = soup.find_all("a",{"class":"pagination__next-link"})
            for next in nexts:
                if not next.get("href"):
                    next_page = False

    def scrap_url_bbc(self, url):
        soup = self.get_response(url)
        article_text = ""
        texts = soup.find_all("div",{"class":"ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0"})
        for text in texts:
            article_text += text.text + "\n"
        return article_text

    def scrape_bbc(self):
        soup = self.get_response("https://www.bbc.com/news")
        articles = soup.find_all("a",{"class":"gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"})
        for article in articles:
            url = "https://www.bbc.com/" + article["href"]
            url_id, check = self.add_url(url, self.webbsite)
            if check:
                text = self.scrap_url_bbc(url)
                if text:
                    words_freq = self.text_to_words(text)
                    self.add_words_to_url(words_freq, url_id)
            self.add_date_to_url(self.date_list[1], url_id)
                       
    def scrap_url_appnews(self, url):
        soup = self.get_response(url)
        article_text = ""

        articles = soup.find("div",{"class":"Article"})
        if articles:
            texts = articles.find_all("p")
            for text in texts:
                article_text += text.text + "\n"
            return article_text

    def scrape_appnews(self):
        # initialize the driver and load the page
        driver = webdriver.Chrome()
        driver.get("https://apnews.com")
        # simulate scrolling down the page until the end
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # wait for the page to load
            time.sleep(3)
            # calculate the new scroll height and check if it has changed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
            # Create a BeautifulSoup object from the response content
            soup = BeautifulSoup(driver.page_source, "html.parser")
            urls = soup.find_all(href=re.compile("/article/"))
            for url in urls:
                url = url["href"]
                if url[:9] == "/article/":
                    url = "https://apnews.com" + url
                url_id, check = self.add_url(url, self.webbsite)
                if check:
                    text = self.scrap_url_appnews(url)
                    if text:
                        words_freq = self.text_to_words(text)
                        self.add_words_to_url(words_freq, url_id)
                self.add_date_to_url(self.date_list[1], url_id)

    def scrape_other_url(self, url):
        soup = self.get_response(url)


    def scrape_other_website(self):
        soup = self.get_response(self.webbsite_url)
        urls = soup.find_all(href=re.compile(self.webbsite_url))
        for url in urls:
            url_id, check = self.add_url(url, self.webbsite)
            if check:
                text = self.scrape_other_url(url)
                if text:
                    words_freq = self.text_to_words(text)
                    self.add_words_to_url(words_freq, url_id)
            self.add_date_to_url(self.date_list[1], url_id)


