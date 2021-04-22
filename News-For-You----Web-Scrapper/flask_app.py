from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from urllib.error import HTTPError

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])  # route with allowed methods as POST and GET
def index():
    review = []
    try:
        if request.method == 'POST':
            searchString = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form
            url = 'https://www.indiatvnews.com/topic/' + searchString
            Uclient = uReq(url)
            Data = Uclient.read()
            Uclient.close()
            html = bs(Data, "html.parser")
            NEWS = html.find("ul", {"class": "newsListfull"})
            all_news = NEWS.find_all("li")
            all_news = all_news[:5]
            review.append(all_news)

            url = 'https://www.indiatoday.in/topic/' + searchString + "/ALL"
            Uclient = uReq(url)
            Data = Uclient.read()
            html = bs(Data, "html.parser")
            NEWS = html.find("div", {"class": "view-content"})
            if NEWS:
                List = NEWS.find_all("li")
                List_News = [news.text for news in List if news.text != "" and isinstance(news.text, str)]
                List_News = List_News[:5]
                review.append(List_News)

            url = 'https://indianexpress.com/?s=Rajasthan'
            Uclient = uReq(url)
            Data = Uclient.read()
            html = bs(Data, "html.parser")
            x = html.find("div", {"class": "search-result"})
            details = x.find_all("div", {"class": "details"})[:5]
            review.append(details)

            return render_template('results.html', reviews=review)  # showing the review to the user
        else:
            return render_template('index.html')
    except HTTPError as e:
        return render_template('404.html')



if __name__ == "__main__":
    app.run(port=8000, debug=True)
