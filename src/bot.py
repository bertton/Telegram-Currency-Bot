import config
import logging
from telethon import TelegramClient, events
from utils.price_parser import parse_currency
from providers import fixer, google

# region setup
logging.basicConfig(level=logging.INFO)

API_ID: int = config.API_ID
API_HASH: str = config.API_HASH
TOKEN: str = config.TOKEN

FIXER_KEY: str = config.FIXER_KEY

bot = TelegramClient('curbottg', API_ID, API_HASH)
bot.start(bot_token=TOKEN)
# endregion setup

# region start
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


@bot.on(events.NewMessage)
async def start(event):
    await event.reply(START_TEXT, link_preview=False)


# endregion start

# region inline
@bot.on(events.InlineQuery)
async def convert(event):
    builder = event.builder
    text = event.text
    api = await fixer.convert(text)
    if not api:
        api = await google.convert(text)
    if api:
        result, date = api
        await event.answer([builder.article(title=result, description=date,
                                            text=f"{result}\n**Last updated ·** `{date}`")],
                           cache_time=30 * 60)
    else:
        await event.answer([await builder.article(title="Invalid Query!", description="Click to learn more!",
                                                  text=START_TEXT)])


# endregion inline

if __name__ == '__main__':
    bot.run_until_disconnected()
