import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from redditAPI import Api

import datetime

import sqlite3 as lite
from sqlalchemy import create_engine

# nltk.download('vader_lexicon')

class Sentiment:
    def __init__(self):
        self.api = Api('UIUC') 
        
        # numdays = 365 * 10 
        numdays = 1
        base = datetime.datetime.today() - datetime.timedelta(days=1)
        # base = datetime.date(2018,4,17) - datetime.timedelta(days=1)
        date_list = [base - datetime.timedelta(days=x) 
                     for x in range(0, numdays)]

        db_conn = create_engine('sqlite:///data.db')
        conn = db_conn.connect()
        for d in date_list:
            string_date = datetime.date(d.year, d.month, d.day)
            c = conn.execute('''select dt from reddit_data where dt=?''',(string_date))
            if(c.fetchone()):
                print('already have data for : ' + str(string_date))
                continue
            
            sentiment, tot_comments = self.sentiment_for_day(d)
            self.write_sentiment_to_db(sentiment,d.strftime('%Y-%m-%d'), tot_comments)
            print(d, sentiment, tot_comments)

    """ returns tuple (sentiment, total comments) """
    def sentiment_for_day(self, d):
        sid = SentimentIntensityAnalyzer()
        posts = self.api.get_comments_for_one_day(d.year, d.month, d.day)
        
        tot_comments = sum([len(p) for p in posts])
        sents = []
        for post in posts:
            tokens = sum([self.tokenize(c) for c in post], [])
            score = sid.polarity_scores(' '.join(tokens))['compound']
            weight = len(post) / tot_comments
            sents.append(score * weight)

        return [sum(sents), tot_comments]
        
    def write_sentiment_to_db(self, sentiment, dt, numComments):
        db_conn = create_engine('sqlite:///data.db')
        conn = db_conn.connect()
        conn.execute('''insert into 
                       reddit_data(dt,sentiment,numComments)
                       values(?,?,?)''', dt, sentiment, numComments)

         
    def tokenize(self, sentence):
        return [w.lower() for w in nltk.word_tokenize(sentence) 
                if w.isalpha() 
                and w.lower() not in stopwords.words('english')]
    
    def lemmatizer(self, sentence):
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(w) for w in sentence]

    def stem(self, sentence):
        porter = nltk.PorterStemmer()
        return [porter.stem(w) for w in sentence]

if __name__ == '__main__':
    Sentiment()
