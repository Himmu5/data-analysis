from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.espncricinfo.com/",
    "Connection": "keep-alive",
    "DNT": "1",  # Do Not Track
    "Upgrade-Insecure-Requests": "1",
}


class Scrapper:
    url = 'https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2022-23-14450'

    def __init__(self):
      pass
    
    def scrap_cricket_data(self):
        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(response.content.decode('utf-8'))
            return # Exit if the request was not successful
        html_content = response.content
        print(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find('div', class_="ds-grow")
        print(divs)
        if divs:
            for div in divs:
               print(div)
        else:
            print("Could not find the specified div element.")
        
    def headless_browser_scrapper(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                "--disable-blink-features=AutomationControlled"
            ])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36",
                java_script_enabled=True,
            )

            page = context.new_page()
            page.goto(self.url, wait_until="networkidle")

            html = page.content()
            print(html)
            soup = BeautifulSoup(html, "html.parser")
            print(soup.prettify()[:1000])  # preview content

            for row in soup.select("table tbody tr"):
                cols = [c.get_text(strip=True) for c in row.find_all("td")]
                print(cols)

            browser.close()