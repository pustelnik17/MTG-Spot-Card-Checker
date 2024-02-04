from urllib.parse import quote
import re
import httpx
import asyncio
import json

class Data:
    def __init__(self, inputFilePath="data.txt", offerLimit=50):
        self.cards = Data.GetCards(inputFilePath)
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
                if card["data"][offerId]["stock"] > 0 and card["data"][offerId]["rarity"] != "Tip Card":
                    prices.append(card["data"][offerId]["price"])
            result.append(min(prices) if len(prices) > 0 else -1)
        return [{"names": self.cards[i], "cost": result[i]} for i in range(len(self.cards))]

    @staticmethod
    def GetCards(path):
        with open(path) as file:
            result = [element.strip() for element in file.readlines()]
            for cardId in range(len(result)):
                result[cardId] = re.sub("^[0-9]* ", "", result[cardId])
            return result

def main():
    data = Data(inputFilePath="data.txt")
    print(data.result)


if __name__ == "__main__":
    main()