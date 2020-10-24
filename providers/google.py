import aiohttp

from bs4 import BeautifulSoup

import utils

URL = "https://google.com/search?q="

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

async def convert(query):
    query = query.replace(' ', '+')
    async with aiohttp.ClientSession() as session:
        async with session.get(URL + query, headers=HEADERS) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                res = soup.find_all('div', class_='b1hJbf')
                if res:
                    date_res = soup.find('div', class_='hqAUc')
                    date = BeautifulSoup(str(date_res), "html.parser")
                    update_date = date.get_text().split("·")[0]
                    soup = BeautifulSoup(str(res[0]), "html.parser")
                    soup_text = soup.get_text().replace('equals', ' => ')
                    return soup_text, utils.datetime_from_str(update_date)