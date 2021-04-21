from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
    review = []
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        url = 'https://www.indiatvnews.com/topic/' + searchString
        Uclient = uReq(url)
        Data = Uclient.read()
        Uclient.close()
        html = bs(Data, "html.parser")
        NEWS = html.find("ul", {"class": "newsListfull"})
        all_news = NEWS.find_all("li")
        all_news = all_news[:5]
        review.append(all_news)

        url = 'https://www.indiatoday.in/topic/' + searchString +"/ALL"
        Uclient = uReq(url)
        Data = Uclient.read()
        html = bs(Data, "html.parser")
        NEWS = html.find("div", {"class": "view-content"})
        List = NEWS.find_all("li")
        List_News = [news.text for news in List if news.text != ""]
        List_News = List_News[:5]
        review.append(List_News)

        url = 'https://www.bbc.co.uk/search?q=' + searchString
        Uclient = uReq(url)
        Data = Uclient.read()
        html = bs(Data, "html.parser")
        News = html.find("ul", {"class": "ssrcss-1v7bxtk-StyledContainer enjd40x0"})
        if News:
            L = News.find_all("li")
            l = [str(i.a.text + i.find_all("p")[1].text) for i in L]
            l = l[:5]
            review.append(l)
            for i in L:
                print(i.a.text)
                text = i.find_all("p")
                print(text[1].text)

        url = 'https://indianexpress.com/?s=Rajasthan'
        Uclient = uReq(url)
        Data = Uclient.read()
        html = bs(Data, "html.parser")
        x = html.find("div", {"class": "search-result"})
        details = x.find_all("div", {"class": "details"})[:5]
        review.append(details)

        #review = [all_news,List_News,l,details,searchString]
        return render_template('results.html', reviews=review) # showing the review to the user
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000