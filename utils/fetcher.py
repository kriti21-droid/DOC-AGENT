import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_article_text(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/115.0.0.0 Safari/537.36",
                locale='en-US',
                timezone_id='America/New_York',
                viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()
            page.goto(url, timeout=60000)
            time.sleep(7)  # Wait for JS to load & verification
            
            content = page.query_selector('div.article-body, div.article-content')
            if content:
                article_text = content.inner_text()
                browser.close()
                return article_text.strip(), None
            
            html = page.content()
            browser.close()
            
            soup = BeautifulSoup(html, 'html.parser')
            main = soup.find('main')
            if main:
                return main.get_text(separator="\n", strip=True), None
            else:
                return soup.get_text(separator="\n", strip=True), None
    except Exception as e:
        return "", f"Exception occurred: {str(e)}"
