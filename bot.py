import datetime
import logging
import os

import aiohttp
import telethon

from bs4 import BeautifulSoup
from providers import fixer, google

logging.basicConfig(level=logging.INFO)

START_TEXT = """
I'm an inline currency converter bot to help you easily convert any currency to another. 
I support over 100 currencies and advanced queries with the help of Google's search AI.

**How to use me:**

Type my username following by the currency you want to convert from following the target currency.

Eg: `@currconverter_bot 20 EUR in USD`

Or if you don't remember what currency does a country uses you can use countries names instead of the currency name:

Eg: `@currconverter_bot 20 European Money in Nigeria`

**Donate:**

If you like my bot you can help me with a small donation at:

· [PayPal](https://www.paypal.com/paypalme/marcelalexandrunitan)
· [Revolut](http://pay.revolut.com/profile/marceli6p)

**Source Code:** 
· [GitHub](https://github.com/nitanmarcel/Telegram-Currency-Bot)

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

API_ID: str = 0
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


@bot.on(telethon.events.InlineQuery)
async def convert(event):
    builder = event.builder
    text = event.text

    if not text:
        return await event.answer([], switch_pm='How to use me!', switch_pm_param='_')

    api = await fixer.convert(text)
    if not api:
        api = await google.convert(text)

    if api:
        result, date = api
        await event.answer(
            [await builder.article(title=result, text=f"{result} **\nLast updated ·** `{date.strftime('%Y-%m-%d %H:%M')}`")]
            ,
            cache_time=30 * 60)
    else:
        await event.answer([await builder.article(title="Invalid Query!", description="Click to learn more!",
                                                  text="An invalid query was given. Make sure you entered your query "
                                                       "in the following format: `{amount} {from currency} {to "
                                                       "currency}`.")])


@bot.on(telethon.events.NewMessage)
async def start(event):
    await event.reply(START_TEXT, link_preview=False)


if __name__ == "__main__":
    bot.run_until_disconnected()
