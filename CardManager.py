from urllib.parse import quote
import httpx
import asyncio
import json

class Data:
    def __init__(self, cards, upperBound=None, offerLimit=50):
        self.cards = cards
        self.upperBound = upperBound
        self.cardsJSON = asyncio.run(Data.Fetch(self, offerLimit))
        self.result = Data.GetMinimalCostOffers(self)

    async def Fetch(self, limit):
        timeout = httpx.Timeout(10.0, read=None)
        async with httpx.AsyncClient() as client:
            reqs = [client.get("https://mtgspot.cn-panel.pl/products?s_title=" + quote(card) + f"&limit={limit}&offset=0&order_by=price&sort_by=asc", timeout=timeout) for card in self.cards]
            result = await asyncio.gather(*reqs)
        return [json.loads(element.text) for element in result]

    def GetMinimalCostOffers(self):
        result = []
        for card in self.cardsJSON:
            prices = []
            for offerId in range(len(card["data"])):
                if card["data"][offerId]["stock"] > 0 and card["data"][offerId]["rarity"] != "Tip Card" and float(card["data"][offerId]["price"]) <= self.upperBound:
                    prices.append(float(card["data"][offerId]["price"]))
            result.append(min(prices) if len(prices) > 0 else -1)
        return [{"name": self.cards[i], "cost": result[i]} for i in range(len(self.cards))]
