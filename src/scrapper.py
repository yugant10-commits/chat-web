import requests
from bs4 import BeautifulSoup
import pandas as pd
from sentence_transformers import SentenceTransformer
import re

class ScrapeWebPage:
    """Scrapes the Web page and processes it as required.
    """
    def __init__(self, url) -> None:
        self.url =url
    
    
    def get_url(self):
        reqs = requests.get(self.url)
        soup = BeautifulSoup(reqs.text, "html.parser")
        urls = []
        for link in soup.find_all("a"):
            urls.append(link.get("href"))
        return urls    
     
    def get_page_contents(self, url_list:list):
        new_url_list = [url for url in url_list if "#" not in url]
        process_list = [url for url in new_url_list if url.startswith("https://tai.com.np")]
        pages=[]
        for link in process_list:
            try:
                print(f"Processing link: {link}")
                request = requests.get(link)
                scraped_data = BeautifulSoup(request.text, "html.parser")
                filtered_text = scraped_data.text
                cleaned_text = ScrapeWebPage.remove_whitespace(filtered_text)
                pages.append({
                    "text": cleaned_text,
                    "source": link
                }) 
            except Exception as e:
                print("Invalid URL: ", link)
        return pages
    @staticmethod
    def remove_whitespace(text:str):
        pattern = r"\s+"
        s = re.sub(pattern, " ", text)
        return s
    

# tai_scraper = ScrapeWebPage("https://www.wiseadmit.io/blogs")
# url_list = tai_scraper.get_url()
# content = tai_scraper.get_page_contents(url_list = url_list)
# print(url_list)
