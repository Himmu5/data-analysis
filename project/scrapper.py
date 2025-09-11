from bs4 import BeautifulSoup
import requests

class Scrapper:
    url = 'https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2022-23-14450'

    def __init__(self):
      pass
    
    def scrap_cricket_data(self):
        response = requests.get(self.url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup)
