## Project McNulty
###### Week 4 - Week 6.5

![](mcnulty.jpg)

#### Back story:

Using data from the web (API or scraped) or one of the optional supplied data sets (possibly in conjunction with your own data), create models using supervised learning techniques. Extend your findings with a flask website and/or OPTIONAL D3 visualization.

Note you can work as a 'group' (with other folks working on the same data source as you) for 
brainstorming, design, additional data, etc. However, the final projects will be individual.


#### About:

My Project McNulty scrapes book ratings from Goodreads, using headless Selenium scrapers on AWS to speed up the processing, generating 1.2 million data points which are fed into a Surprise based recommender system to locate books which would be well liked, if they were read.  Finally, a bokeh app hosted on AWS provides an interactive visualization for exploring books.