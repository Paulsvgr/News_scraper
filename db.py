from contextlib import contextmanager
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import date as date_now
from create_db import *
import shutil

class Database():
    # This class allows connection with the databas
    def __init__(self) -> None: 
        # Make a copy of the database file
        shutil.copy2('scrap_data.db', 'scrap_data backup.db')
        # Create an engine that connects to your database
        engine = create_engine('sqlite:///scrap_data.db')
        # Create a session
        self.Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    @contextmanager
    def session_scope(self):
        # this function is used to manage any error when connecting with the db
        try:
            session = self.Session()
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {str(e)}")
        finally:
            session.close()
 
    def add_news_category(self, category_name):
        # Adds a news category to the database
        # Return true if its succeeded otherway False

        with self.session_scope() as session:
            # Check if the category already exists
            category = session.query(NewsCategory).filter_by(news_category=category_name).first()
            if category is not None:
                return False
            else:
                # Create a new category
                category = NewsCategory(news_category=category_name)
                session.add(category)
                return True

    def add_word_to_category(self, word, news_category):
        # Adds a word to the database
        # Return true if its succeeded otherway False

        with self.session_scope() as session:
            # Check if the word already exists in the Searching_words table
            new_word = session.query(Searching_words).filter(word == word).first()

            # If the word does not exist, create a new Searching_words object
            if new_word is not None:
                new_word = Searching_words(word=word)
                session.add(new_word)
                session.flush()
            else:
                return False

            # Adds the new row to the WordsCategorized table
            new_word_category = Words_cathegorized(news_category_id=news_category, word_id=new_word.id)
            session.add(new_word_category)
            return True

    def get_all_categories(self):
        # Returns a list of all existing news categories.

        with self.session_scope() as session:
            categories = session.query(NewsCategory).all()
            return [[category.news_category, category.id] for category in categories]

    def check_if_found(self, word):
        # Returns a list of all existing words.

        with self.session_scope() as session:
            words = session.query(Words).filter_by(word=word).first()
            return words

    def get_dates(self):
        # Returns a list of all dates.

        with self.session_scope() as session:
            dates = session.query(Dates).all()
            return [[date.date, date.id] for date in dates]
    
    def get_searching_words(self):
        # Returns a dictionary of the searching words as value of their cathegory.

        with self.session_scope() as session:
            all_words= {}
            # list of all cathegories
            categories = session.query(NewsCategory).all()
            for category in categories:
                words = session.query(Searching_words).select_from(Words_cathegorized).join(Words_cathegorized.word).join(Words_cathegorized.news_category).filter(NewsCategory.id == category.id).all()
                all_words[category.news_category] = [word.word for word in words]
            return all_words

    def add_website(self, website_name, website_url):
        # Adds a webbsite to the database
        # Return messages if its succeeded returns True also if not False 

        with self.session_scope() as session:
            # Check if website name oçor url already exists in the database
            website = session.query(Websites).filter_by(website=website_name).first()
            website2 = session.query(Websites).filter_by(website_url=website_url).first()
            if website is not None:
                return f"{website_name} already exists in the database.", False
            if website2 is not None:
                return f"{website_url} already exists in the database.", False
            else:
                # Create a new website object and add it to the session
                website = Websites(website=website_name, website_url=website_url)
                session.add(website)
                return f"{website_name} added to the database.", True
            
    def check_latest_date(self):
        # Returns the latest added date

        with self.session_scope() as session:
            dates = session.query(Dates).all()
            return dates[-1].date

    def add_current_date(self):
        # Adds a date to the db
        # returns list of all dates and True if succeeded False if not

        with self.session_scope() as session:
            # Check if a record with the current date already exists
            date = session.query(Dates).filter(func.date(Dates.date) == date_now.today()).first()
            if not date:
                # If not, add a new record with the current date
                date = Dates(date=date_now.today())
                session.add(date)
                session.flush()
                return [date.date, date.id], True
            return [date.date, date.id], False

    def add_url(self, url, website):
        # Adds a url to the db
        # Returns url_id with true if it didnt already exists
        
        with self.session_scope() as session:
            # Check if the URL already exists in the database
            url_obj = session.query(URLs).filter(URLs.url == url).first()
            #website = session.query(Websites).filter(website == website).first()

            if not url_obj:
                # URL doesn't exist in the database, create a new URL object
                url_obj = URLs(url=url, website_id=website)
                session.add(url_obj)
                session.flush()
                return [url_obj.id, True]
            return [url_obj.id, False]

    def get_webbsite(self, website):
        # Returns website name, id, url

        with self.session_scope() as session:
            website = session.query(Websites).filter_by(website=website).first()
            return [website.website, website.id, website.website_url]

    def get_all_websites(self):
        # Returns a list of list of all website name, id, url

        with self.session_scope() as session:
            websites_obj = session.query(Websites).all()
            return [[website.website, website.id, website.website_url] for website in websites_obj]

    def get_cathegories(self):
        # Returns a list of  of list of all news cathegory name and id

        with self.session_scope() as session:
            news_categories = session.query(NewsCategory).all()
            return [[news_category.news_category, news_category.id] for news_category in news_categories]

    def add_date_to_url(self, date, url):
        # Adds a date url relation

        print("Url searched done")
        with self.session_scope() as session:
            existing_scrape = session.query(Scrapes).filter_by(date_id=date, url_id=url).first()
            if not existing_scrape:
                # Create a new Word_in_url object and add it to the session
                date_url = Scrapes(url_id=url, date_id=date)
                session.add(date_url)

    def add_words_to_url(self, words_freq, url_id):
        # Adds the words in the url article 
        with self.session_scope() as session:
            # Loop through the filtered words add and update the counts
            for word in words_freq.keys():
                word_obj = session.query(Words).filter_by(word=word).first()
                if not word_obj:
                    word_obj = Words(word=word)
                    session.add(word_obj)
                    session.flush()
                # Create a new word_in_url object and add it to the session
                word_url = Word_in_url(word_id=word_obj.id, url_id=url_id, count=words_freq[word])
                session.add(word_url)

    def get_all_urls(self):
        # Returns a list of all url, id 
        with self.session_scope() as session:
            urls_obj = session.query(URLs).all()
            return [[url.url, url.id] for url in urls_obj]

    def get_urls_by_date(self, date_id):
        # Returns a list of all urls in a given date
        with self.session_scope() as session:
            urls = session.query(URLs).join(Scrapes).filter(Scrapes.date_id == date_id).all()
            return [[url.url, url.id] for url in urls] 
