from urllib.parse import quote
from urllib3 import PoolManager

def GetCards(path):
    with open(path) as file:
        return [element.strip() for element in file.readlines()]
def GetJSON(name, http):
    response = http.request("GET", "https://mtgspot.cn-panel.pl/products?s_title=" + quote(name) + "&limit=25&offset=0&order_by=price&sort_by=asc")
    return response.json()
def InStock(item):
    if item["rarity"] != "Tip Card" and item["stock"] > 0:
        return True
    return False
def main():
    http = PoolManager()
    cardList = GetCards("data.txt")
    result = dict.fromkeys(cardList)
    offer = [GetJSON(card, http) for card in cardList]
    for cardIterator in offer:
        for item in cardIterator["data"]:
            if InStock(item):
                result[item["title"]] = item["price"]
                break
    for element in result:
        print(element, " ---> ", result[element])


if __name__ == "__main__":
    main()