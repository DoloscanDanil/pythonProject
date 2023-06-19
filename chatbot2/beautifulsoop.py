import requests
from bs4 import BeautifulSoup


def computers():
    response = requests.get("https://999.md/ru/list/phone-and-communication/mobile-phones")
    response = requests.get("https://999.md/ru/list/computers-and-office-equipment/desktop-computers")
    soup = BeautifulSoup(response.text, "html.parser")

    news_articles = soup.find_all("li", class_="ads-list-photo-item")
    computers = []
    for article in news_articles:
        try:
            if article:
                title = article.find("div", class_="ads-list-photo-item-title").text
                image = article.find("img")["src"]
                link = article.find("a")["href"]

                print(title)
                print(image)
                print("https://999.md/" + link)
                computers.append("https://999.md/" + link)
        except:
            pass

    return computers


