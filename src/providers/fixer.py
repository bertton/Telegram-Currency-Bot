import aiohttp
from config import FIXER_KEY
from utils.price_parser import parse_currency, format_currency
from utils.currencies import  _currencies
from utils.date_parser import format_datetime

async def convert(query):
    currency = parse_currency(query)
    if not currency:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://data.fixer.io/api/convert?access_key={FIXER_KEY}&from={currency.from_currency}&to={currency.to_currency}&amount={currency.amount}") as response:
            if response.status == 200:
                js = await response.json()
                result = js["result"]
                query = js["query"]
                date = js["info"]["timestamp"]

                frmt_amount = format_currency(query['amount'])
                frmt_result = format_currency(result)
                frmt_from = _currencies[currency.from_currency]
                frmt_to = _currencies[currency.to_currency]
                frmt_date = format_datetime(date)
                return f"{frmt_amount} {frmt_from} => {frmt_result} {frmt_to}", frmt_date