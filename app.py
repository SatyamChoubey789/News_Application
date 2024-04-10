# import libraries 
from flask import Flask, render_template, request 
from newsapi import NewsApiClient 
import random

# init flask app 
app = Flask(__name__) 

# Init news api 
newsapi = NewsApiClient(api_key='b8f066dde0ac41c58a79dfdd40768e90') 

# helper function 
def get_sources_and_domains(): 
    all_sources = newsapi.get_sources()['sources'] 
    sources = [] 
    domains = [] 
    for e in all_sources: 
        id = e['id'] 
        domain = e['url'].replace("http://", "") 
        domain = domain.replace("https://", "") 
        domain = domain.replace("www.", "") 
        slash = domain.find('/') 
        if slash != -1: 
            domain = domain[:slash] 
        sources.append(id) 
        domains.append(domain) 
    sources = ", ".join(sources) 
    domains = ", ".join(domains) 
    return sources, domains 

@app.route("/", methods=['GET', 'POST']) 
def home(): 
    if request.method == "POST": 
        keyword = request.form["keyword"] 
        all_articles = newsapi.get_everything(q=keyword, language='en')['articles'] 
        random.shuffle(all_articles)  # Shuffle the list of articles
        return render_template("home.html", all_articles=all_articles, keyword=keyword) 
    else: 
        top_headlines = newsapi.get_top_headlines(country="in", language="en") 
        all_headlines = top_headlines['articles'] 
        random.shuffle(all_headlines)  # Shuffle the list of articles
        return render_template("home.html", all_headlines=all_headlines) 
    return render_template("home.html")

if __name__ == "__main__": 
    app.run(debug=True)
