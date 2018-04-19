import requests
import praw
import time
from datetime import datetime, date, timedelta

class Api:
    def __init__(self, subreddit = None):
        auth = eval(open('.env', 'r').read())
        
        self.reddit = praw.Reddit(client_id=auth['CLIENT_ID'],
                             client_secret=auth['CLIENT_SECRET'],
                             password=auth['PASSWORD'],
                             user_agent=auth['USERAGENT'],
                             username=auth['USERNAME'])

        self.subreddit = self.reddit.subreddit(subreddit)

    def utc_to_unix_time(self, t):
        """ convert string into datetime, t =\' year-month-day\' 
        """
        (y,m,d) = str(t).split('-')
        return datetime(int(y), int(m), int(d)).strftime('%s')
    
    def get_comments_for_one_day(self, y,m,d):
        """ given one day, get the full days comments
        """
        in_date = date(y,m,d)

        start = self.utc_to_unix_time(in_date - timedelta(1)) 
        end = self.utc_to_unix_time(in_date) 
        return self.get_comments_between(start,end)

    def get_post_ids(self, start_date, end_date):
        response = requests.get('https://api.pushshift.io/reddit/submission/search/?after='+start_date+'&before='+ end_date +'&subreddit=UIUC')
        return [p['id'] for p in response.json()['data']]


    def get_comments_between(self, start_date, end_date):
        """ get comments between two dates, 
            args needs to be in unix timestamp
        """
        ret = []
        ids = self.get_post_ids(start_date, end_date)

        for id in ids:
            comments = self.reddit.submission(id).comments
            ret.append(self.get_nested_comments(comments))
        return ret

    def get_nested_comments(self, comments):
        tmp = []
        for comment in comments:
            if isinstance(comment, praw.models.MoreComments):
                return self.get_nested_comments(comment.comments(update=True))
            elif(comment):
                tmp.append(comment.body)
        return tmp

# api = Api('UIUC')
# # start_time, end_time = datetime.date(2016,1,1), datetime.date(2016,1,2)
# # s = api.utc_to_unix_time(dt.datetime.now().date() - timedelta(1)) 
# # e = api.utc_to_unix_time(dt.datetime.now().date()) 
# print(api.utc_to_unix_time('2014-2-3'))
# print(api.get_comments_for_one_day(2017,1,1))
# print(api.get_comments_between(s,e))
