from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func, Table, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# create engine and connect to SQLite database
engine = create_engine('sqlite:///scrap_data.db', echo=True)

# create declarative base
Base = declarative_base()

class NewsCategory(Base):
    __tablename__ = 'news_categories'
    id = Column(Integer, primary_key=True)
    news_category = Column(String(20), nullable=False)

class Words_cathegorized(Base):
    __tablename__ = 'words_cathegorized'
    id = Column(Integer, primary_key=True)
    news_category_id = Column(Integer, ForeignKey('news_categories.id'), nullable=False)
    word_id = Column(Integer, ForeignKey('searching_words.id'),  nullable=False)
    news_category = relationship('NewsCategory', cascade="all, delete", backref='words_cathegorized')
    word = relationship('Searching_words', cascade="all, delete", backref='words_cathegorized')

class Searching_words(Base):
    __tablename__ = 'searching_words'
    id = Column(Integer, primary_key=True)
    word = Column(String(100), nullable=False)

class Websites(Base):
    __tablename__ = 'websites'
    id = Column(Integer, primary_key=True)
    website = Column(String(20), nullable=False)
    website_url = Column(String(1000))

class URLs(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String(1000), nullable=False)
    website_id = Column(Integer, ForeignKey('websites.id'), nullable=False)
    website = relationship('Websites', cascade="all, delete", backref='urls')

class Scrapes(Base):
    __tablename__ = 'scrapes'
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'), nullable=False)
    date_id = Column(Integer, ForeignKey('dates.id'), nullable=False)
    url = relationship('URLs', cascade="all, delete", backref='scrapes')
    date = relationship('Dates', cascade="all, delete", backref='scrapes')

class Dates(Base):
    __tablename__ = 'dates'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.today().date())

# Define the words table
class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)

class Word_in_url(Base):
    __tablename__ = 'word_in_url'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)
    url_id = Column(Integer, ForeignKey('urls.id'),  nullable=False)
    count = Column(Integer, nullable=False, default=1)
    word = relationship('Words', cascade="all, delete", backref='word_in_url')
    url = relationship('URLs', cascade="all, delete", backref='word_in_url')



# create tables
Base.metadata.create_all(engine)

# Define a list to store the new NewsCategory objects to add
news_categories = {
    "Politics": ["government", "political", "party", "elections", "law", "leader", "policy", "congress", "president"],
    "Sports": ["game", "team", "player", "sports", "championship", "match", "score", "league", "training"],
    "Entertainment": ["entertainment", "music", "film", "actor", "awards", "television", "show", "performance", "director"],
    "Technology": ["technology", "digital", "innovation", "devices", "software", "internet", "data", "artificial intelligence", "cybersecurity"],
    "Business": ["business", "economy", "companies", "market", "trade", "investment", "finance", "industry", "entrepreneur"],
    "Health": ["health", "medical", "disease", "care", "research", "doctor", "hospital", "medicine", "healthcare"],
    "Science": ["science", "research", "technology", "discovery", "studies", "innovation", "astronomy", "biology", "physics"],
    "Environment": ["environment", "nature", "climate", "green", "conservation", "pollution", "sustainability", "wildlife", "ecology"],
    "World news": ["world", "international", "news", "global", "country", "region", "politics", "economy", "culture"],
    "Crime": ["crime", "police", "investigation", "arrest", "court", "justice", "law enforcement", "incident", "homicide"],
    "Disaster": ["disaster", "emergency", "relief", "aid", "response", "natural", "hurricane", "earthquake", "tsunami"],
}
def create():
    Session = sessionmaker(bind=engine)

    with Session() as session:

        # Loop over the dictionary and create new NewsCategory objects
        for category, words in news_categories.items():
            # Create a new NewsCategory object
            new_category = NewsCategory(news_category=category)
            # Add the new NewsCategory object to the session
            session.add(new_category)
            session.commit()
            # Add the words for this category to the words table
            for word in words:
                # Create a new Word object and associate it with the new category
                new_word = Searching_words(word=word)
                # Add the new Word object to the session
                session.add(new_word)
                session.commit()
                new_word_cath = Words_cathegorized(news_category_id=new_category.id,word_id=new_word.id)

                session.add(new_word_cath)

        # Commit the transaction to the database
        session.commit()
        websites = ["https://www.huffpost.com", 'https://www.bbc.com', 'https://apnews.com']
        for website_url in websites:
            # Check if website already exists in the database
            website_name_split_www = website_url.split("https://www.")
            if len(website_name_split_www) == 1:
                website_name_split_www = website_url.split("https://")
                if len(website_name_split_www) == 1:
                    website_name_split_www = website_name_split_www[0]                 
            website_name = website_name_split_www[1].split(".")[0]
            website_name = website_name.title()
            website = session.query(Websites).filter_by(website=website_name).first()
            website2 = session.query(Websites).filter_by(website_url=website_url).first()
            if website:
                print(f"{website_name} already exists in the database.")
            elif website2:
                print(f"{website_url} already exists in the database.")
            else:
                # Create a new website object and add it to the session
                website = Websites(website=website_name, website_url=website_url)
                session.add(website)
                print(f"{website_name} added to the database.")
        
        session.commit()

def delet_data():
    Session = sessionmaker(bind=engine)

    with Session() as session:
        try:
            session.query(Dates).delete()
            session.query(URLs).delete()
            session.query(Scrapes).delete()
            session.commit()
        except:
            session.rollback()

# Session = sessionmaker(bind=engine) 
# # create a metadata object to represent your database schema
# metadata = MetaData()
# url_obj = URLs(url="", website_id=1)
# session.add(url_obj)
