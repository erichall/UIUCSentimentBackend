## ABOUT

This project consists of two microservices, one for the backend and one for the frontend. In order to run the program on your local computer you need to clone both projects from github and start them in separate terminals.
![frontend](https://github.com/erichall/UIUCSentimentBackend/blob/master/example_screen.png)

## USAGE

### BACKEND
git clone git@github.com:erichall/UIUCSentimentBackend.git  
cd UIUCSentimentBackend/  
pip install requirements.txt  
python server.py  
OR python server.py --host <HOST, default=localhost> --port <PORT, default=3001> to specify manual host and port.  

test it with opening a browser and navigate to http://localhost:PORT/sentiment_range?start_date=2017-01-01&end_date=2017-02-01
where port is either 3001 or what you specified in the argument above. 

You should see a JSON dump that looks something like this:
{"2017-01-01": {"sentiment": 0.5670441860465116, "post_count": 43}, "2017-01-02": {"sentiment": 0.5536891304347826, "post_count": 46}...

#### BACKEND TROUBLE
##### This site can’t be reached localhost refused to connect.  
  You can have navigated to the wrong address, make sure it’s http://HOST:PORT/sentiment_range?start_date=2017-01-01&end_date=2017-02-01 . Yes you need to sentiment_range endpoint with start and end-date. 


### FRONTEND
git clone git@github.com:erichall/UIUCSentimentFrontend.git  
cd UIUCSentimentFrontend/  
npm install  
REACT_APP_SERVER_HOST=server_host REACT_APP_SERVER_PORT=server_port npm start  

where server_host = the host you started the server on, default localhost
  server_port = the port you started the server on, default 3001  

navigate to http://localhost:3000/ and your browser and you should see a graf with that shows the sentiment over time.  

#### FRONTEND TROUBLE
##### cache problems
The most common problem I encountered is browser caching, so either open the frontend page in incognito mode or clear you browser history.
