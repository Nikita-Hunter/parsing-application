import json
import requests
from bs4 import BeautifulSoup

def get_first_posts():
    headers = {
        "User-Agent":  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    url = "https://naked-science.ru/article/physics"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_card = soup.find_all("div", class_="news-item grid")

    posts_dict = {}
    for article in articles_card:
        article_title = article.find("a", class_="animate-custom").text.strip()
        article_desc = article.find("div", class_="news-item-excerpt").text.strip()
        article_url = article.find("div", class_="news-item-title").find("h3").find("a").get("href")
        article_date_time = article.find("span", class_="echo_date").text.strip()
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]
        #print(f"{article_title} | {article_url} | {article_date_time}")
        posts_dict[article_id] = {
            "article_date_time": article_date_time,
            "article_title": article_title,
            "article_url":article_url,
            "article_desc":article_desc
        }
    with open("posts_dict.json", "w") as file:
        json.dump(posts_dict, file, indent=4, ensure_ascii=False)

def check_posts_update():
    with open("posts_dict.json") as file:
        posts_dict = json.load(file)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    url = "https://naked-science.ru/article/physics"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_card = soup.find_all("div", class_="news-item grid")

    fresh_posts = {

    }

    for article in articles_card:
        article_url = article.find("div", class_="news-item-title").find("h3").find("a").get("href")
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]

        if article_id in posts_dict:
             continue
        else:
            article_title = article.find("a", class_="animate-custom").text.strip()
            article_desc = article.find("div", class_="news-item-excerpt").text.strip()
            article_date_time = article.find("span", class_="echo_date").text.strip()
            posts_dict[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }
            fresh_posts[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }
    with open("posts_dict.json", "w") as file:
        json.dump(posts_dict, file, indent=4, ensure_ascii=False)
    return fresh_posts

def main():
    #get_first_posts()
    print(check_posts_update())


if __name__ == '__main__':
    main()