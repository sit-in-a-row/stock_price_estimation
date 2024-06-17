import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
import re
import time

BASE_URL = "https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=401&date={target_date}&page={target_page_num}"
start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 6, 1)

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_articles_to_file(articles, path):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(articles, json_file, ensure_ascii=False, indent=4)

def fetch_url(url, retries=3, delay=0.3):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}. Retrying ({attempt + 1}/{retries})...")
            attempt += 1
            time.sleep(delay)
    return None

def fetch_articles_for_date(target_date):
    articles = []
    page_num = 1

    while True:
        url = BASE_URL.format(target_date=target_date, target_page_num=page_num)
        response = fetch_url(url)

        if response is None:
            print(f"Failed to fetch articles for date {target_date} after multiple attempts.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        news_list = soup.select('li.newsList > dl > dd > a')

        if not news_list:
            break

        for news in news_list:
            news_url = news['href']
            pattern = r'article_id=(\d+)&office_id=(\d+)'
            match = re.search(pattern, news_url)

            if match:
                article_id = match.group(1)
                office_id = match.group(2)
                article_url = f'https://n.news.naver.com/mnews/article/{office_id}/{article_id}'
                article_response = fetch_url(article_url)

                if article_response is None:
                    print(f"Failed to fetch article {article_url} after multiple attempts.")
                    continue

                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                try:
                    title = article_soup.find('h2', class_='media_end_head_headline').text.strip()
                except AttributeError:
                    title = '정보를 찾을 수 없음'

                try:
                    date = article_soup.find('span', class_='media_end_head_info_datestamp_time _ARTICLE_DATE_TIME').text.strip()
                except AttributeError:
                    date = '정보를 찾을 수 없음'

                try:
                    content = article_soup.find('article', class_='_article_content').text.strip()
                except AttributeError:
                    content = '정보를 찾을 수 없음'

                article_data = {
                    'title': title,
                    'date': date,
                    'content': content
                }

                articles.append(article_data)

        page_num += 1

    return articles

def crawl():
    current_date = start_date

    total_days = (end_date - start_date).days + 1
    completed_days = 0

    while current_date <= end_date:
        year = current_date.strftime('%Y')
        month = current_date.strftime('%m')
        day = current_date.strftime('%d')

        directory_path = f'./news_2/{year}/{month}'
        create_directory(directory_path)

        target_date = current_date.strftime('%Y%m%d')
        articles = fetch_articles_for_date(target_date)

        if articles:
            file_path = f'{directory_path}/{target_date}.json'
            save_articles_to_file(articles, file_path)
            print(f"Saved {len(articles)} articles to {file_path}")
        else:
            print(f"No articles found for date {target_date}")

        completed_days += 1
        progress = (completed_days / total_days) * 100
        print(f"Crawling done for {target_date}. Progress: {progress:.2f}%")

        current_date += timedelta(days=1)

# if __name__ == '__main__':
#     main()

# 실행
crawl()