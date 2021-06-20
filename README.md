# Documentation
In the midst of unprecedented health and humanitarian crises like the COVID-19 pandemic, the media is full of worrying headlines.

+ _Tired of reading disturbing news?_

+ _Do you want to be in control of the news you consume?_

SEAN, Sentiment and Emotion Analyzer for News, is here to help you take ownership of your news feed. SEAN is a REST API for getting news with sentiments and emotions. It makes use of an external API called Newsapi ([Here](https://newsapi.org/) you can find more information about the external api).

You can get positive and uplifting news if you so choose. With the help of SEAN, you can also track the sentiments and emotions of your brand in real time and over time. You can get news with sentiments and emotions by using the following parameters:

## Search Parameters

+ _Keyword(s): You can get, for example, news that contains "Covid-19" by using q parameter._

+ _Keyword(s) in title: You can get, for example, news that contains "Covid-19" in title by using qintitle parameter._


In addition to q and qintitle, you can search news using the following parameters: sources, domains, exclude_domains, from_param(date), to(date), language, sort_by,page, and page_size.

##Project Setup

1. Fork the project from Github
    ~~~
    $ git clone https://github.com/Fassilsis/SEAN-Sentiment and Emotion Analyzer for News
    ~~~
2. Create virtual environment
    ~~~
    c:\>c:\Python35\python -m venv c:\path\to\myenv
    ~~~
3. Install the requirements from requirements.txt
    ~~~
    pip install r requirements.txt
    ~~~
4. Create api_key.py file under NewsApi directory and put your api key form https://newsapi.org/ as shown below.
    ~~~
    api_key="yourapikey"
    ~~~   
   
4. Run sean.py in your terminal
    ~~~
    python sean.py
    ~~~

##Endpoints


**No.** | **HTTP Method**   | **Route** | **Description**
---:|:---:|:---:| ---
1 |**GET** | /news/sentiments | _API to allow users get news with sentiments._
2 |**GET** | /news/good-news | _API to allow users get positive news._
3 |**GET** | /news/emotions' | _API to allow users get news with emotions._
4 |**GET** | /news/happy-news | _API to allow users get happy news._
5 |**GET** | /news/emotions-metadata| _API to allow users get news search history with aggregated sentiment scores_
6 |**GET** | /news/sentiments-metadata| _API to allow users get news search history with aggregated emotion scores_
7 |**POST** | users/register | _API to create SEAN account_
8 |**POST** | users/login | _API to allow users sign in. Returns access token that lets users access to SEAN_
9 |**POST** | users/logout | _API to allow users sign out of SEAN._
10 |**GET** | /users/account-management | _API to get users' SEAN account information._
11 |**PUT** | /users/account-management | _API to allow users edit SEAN account information._
12 |**DELETE** | /users/account-management | _API to allow users delete their SEAN account._
13 |**GET** | /users/search'| _API to allow administrators access all users account information._
