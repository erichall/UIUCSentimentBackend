# Sentiment Analysis for UIUC subreddit

This project consists of two microservices, one for the backend built in python and one for the frontend built in React.
![frontend](https://github.com/erichall/UIUCSentimentBackend/blob/master/example_screen.png)

## OVERVIEW [BACKEND](https://github.com/erichall/UIUCSentimentBackend)
### redditAPI.py
A wrapper around [Praw](https://praw.readthedocs.io/en/latest/) to fetch comments and posts from [UIUC subreddit](reddit.com/r/UIUC/). This wrapper fetches posts and comments between configurable dates and calculates the sentiment value and stores the data in a [sqllite3](https://docs.python.org/2/library/sqlite3.html) database called data.db.
The data inside data.db consists of sentiment and postscounts between 2010 up to 2018. To fetch more data one must create a .env file following the format:  
```
{
    'CLIENT_ID': 'client_id’,
    'CLIENT_SECRET': 'secret_token',
    'PASSWORD': ‘password’,
    'USERAGENT': app_agent,
    'USERNAME': 'reddit username’
}
```
and register the application at [reddit api](https://www.reddit.com/dev/api)

### sentiment.py
This file calculates the sentiments for each comment. This is done by using pythons [NLTK](http://www.nltk.org/) library together with the VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon. Instead of calculating each comment sentiment separate, each comment is weighted by  

```
# num comments in post / # total comments that day * sentiment_for_comment
```

To get the total sentiment for one day, the sum over all sentiment is used for that particular day. 

### server.py
The server provides the backend REST api for the frontend to be able to fetch data for givens dates. This is done with [flask](http://flask.pocoo.org/)


## OVERVIEW [FRONTEND](https://github.com/erichall/UIUCSentimentFrontend)
The frontend is built using React and is using [React chart js 2](https://github.com/jerairrest/react-chartjs-2) for the graph and [airbnb datepicker](https://github.com/airbnb/react-dates) for choosing dates.

## USAGE
In order to run the program on your local computer you need to clone both projects from github and start them in separate terminals.

### BACKEND
```
git clone git@github.com:erichall/UIUCSentimentBackend.git  
cd UIUCSentimentBackend/  
pip install requirements.txt  
python server.py  
OR python server.py --host <HOST, default=localhost> --port <PORT, default=3001> to specify manual host and port.  
```
test it with opening a browser and navigate to 

```http://localhost:PORT/sentiment_range?start_date=2017-01-01&end_date=2017-02-01```

where port is either 3001 or what you specified in the argument above. 

You should see a JSON dump that looks something like this:
```{"2017-01-01": {"sentiment": 0.5670441860465116, "post_count": 43}, "2017-01-02": {"sentiment": 0.5536891304347826, "post_count": 46}...```

#### BACKEND TROUBLE
##### This site can’t be reached localhost refused to connect.  
  You can have navigated to the wrong address, make sure it’s http://HOST:PORT/sentiment_range?start_date=2017-01-01&end_date=2017-02-01 . Yes you need to sentiment_range endpoint with start and end-date. 


### FRONTEND
```
git clone git@github.com:erichall/UIUCSentimentFrontend.git  
cd UIUCSentimentFrontend/  
npm install  
REACT_APP_SERVER_HOST=server_host REACT_APP_SERVER_PORT=server_port npm start  
```
where server_host = the host you started the server on, default localhost
  server_port = the port you started the server on, default 3001  

navigate to ```http://localhost:3000/``` and your browser and you should see a graf with that shows the sentiment over time.  

#### FRONTEND TROUBLE
##### cache problems
The most common problem I encountered is browser caching, so either open the frontend page in incognito mode or clear you browser history.


## CONTRIBUTORS
Eric Hallström hallstrom.eric@gmail.com







