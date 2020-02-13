import datetime
import logging
import os

import aiohttp
import telethon

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

START_TEXT = """

I'm a inline bot to help you convert any currencies. I support over 1000 currencies both real world and crypto.


Just send me an inline query with the text: __20 euro in usd__ or __how much is 20 euro in usd__ and I'll give you the answer. 

If I'm not returning any results just check your query again or try again later.


**Donate:**


 If you like my work you can donate to me using [PayPal](https://www.paypal.me/marcelalexandrunitan).
 For support contact @nitanmarcel!
 
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

API_ID: int = 0
API_HASH: str = ''
TOKEN: str = ''

try:
    API_ID = os.environ["API_ID"]
    API_HASH = os.environ["API_HASH"]
    TOKEN = os.environ["TOKEN"]
except KeyError as e:
    quit(e.args[0] + ' missing from environment variables')

TEST_MODE = os.environ.get('BOT_TEST_MODE', None)

bot = telethon.TelegramClient("curbottg" if not TEST_MODE else 'curbot_test', int(API_ID), API_HASH)
bot.start(bot_token=TOKEN)

URL = "https://google.com/search?q="


def time_until_end_of_day(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min) - dt


async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text(), response.status


@bot.on(telethon.events.InlineQuery)
async def convert(event):
    inline_builder = event.builder
    inline_text = event.text
    inline_results = []

    html = None
    status_code = None

    if inline_text:
        query = inline_text.replace(' ', '+')
        async with aiohttp.ClientSession() as session:
            html, status_code = await fetch(session, URL + query)
            if status_code == 200:
                soup = BeautifulSoup(html, "html.parser")
                res = soup.find_all('div', class_='b1hJbf')
                date_res = soup.find('div', class_='hqAUc')
                date = BeautifulSoup(str(date_res), "html.parser")
                update_date = date.get_text().replace('· Disclaimer', '')

                if res:
                    soup = BeautifulSoup(str(res[0]), "html.parser")
                    soup_text = soup.get_text().replace('equals', ' => ')

                    inline_results.append(
                        await inline_builder.article(title=soup_text, description=soup_text,
                                                     text=soup_text + '**\nLast updated · ' + update_date + '**')
                    )
                else:
                    inline_results.append(await inline_builder.article(title='Invalid Query!', description='Try Again!',
                                                                       text='Invalid Query! Try again!'))
            else:
                inline_results.append(
                    await inline_builder.article(title='ERROR: ' + str(status_code),
                                                 description='ERROR: ' + str(status_code),
                                                 text='ERROR' + str(status_code)))
    else:
        inline_results.append(await inline_builder.article(title='Invalid Query!', description='Try Again!',
                                                           text='Invalid Query! Try again!'))
    await event.answer(inline_results, switch_pm='How to use me!', switch_pm_param='_',
                       cache_time=time_until_end_of_day().seconds)


@bot.on(telethon.events.NewMessage)
async def start(event):
    await event.reply(START_TEXT)


if __name__ == "__main__":
    bot.run_until_disconnected()
