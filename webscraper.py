import requests
from bs4 import BeautifulSoup
from datetime import datetime

SONY_URL_DISC = "https://direct.playstation.com/en-us" \
                "/consoles/console/playstation5-console.3006646"

SONY_URL_DIGI = "https://direct.playstation.com/en-us/" \
                "consoles/console/playstation5-digital-edition-console.3006647"

AMAZON_URL_DISC = "https://www.amazon.ca/" \
                  "PlayStation-5-Console/dp/B08GSC5D9G"

AMAZON_URL_DIGI = "https://www.amazon.ca/Playstation-3005721-" \
                  "PlayStation-Digital-Edition/dp/B08GS1N24H "

CANADACOMP_URL = "https://www.canadacomputers.com/product_info.php?c" \
                 "Path=13_1860_1861_3892&item_id=205551"

GAMESTOP_URL_DISC = "https://www.gamestop.ca/PS5/Games/877522/" \
                    "playstation-5-only-available-for-purchase-in-a-bundle"

GAMESTOP_URL_DIGI = "https://www.gamestop.ca/PS5/Games/877523/playstation-5" \
                    "-digital-edition-only-available-for-purchase-in-a-bundle"


def sony(soup, url):
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    ps = soup.find_all("p")
    ans = ["Sony", "Unavailable", dt, url]
    for p in ps:
        if "Out of Stock" in p:
            return ans
    ans[1] = "Available"
    return ans


def amazon(soup, url):
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    visible_text = soup.getText()
    ans = ["Amazon", "Unavailable", dt, url]
    if "Currently unavailable." in visible_text:
        return ans
    ans[1] = "Available"
    return ans


def canada_computers_parse(soup, url):
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    ps = soup.find_all("p")
    ans = ["Canada Computers", "Unavailable", dt, url]
    for p in ps:
        if "AVAILABLE AT" in p or "AVAILABLE TO" in p:
            ans[1] = "Available"
    return ans


def game_stop_parse(soup, url):
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    all_imgs = soup.find_all('img', src=True)
    ans = ["GameStop", "Unavailable", dt, url]
    for img in all_imgs:
        if "/Content/Images/deliveryAvailable.png" in img['src']:
            ans[1] = "Available"
            return ["GameStop", "Available", dt, url]
    return ans


def main():
    """
    returns a list of websites and ps5 stock availabilities
    format: [['location name,'availability status',,'Date time ',' url',
    'edition' ], ...]

    ex date time: 25/06/2021 07:58:56

    :return: List[List[str]]
    """

    data = []

    website = requests.get(GAMESTOP_URL_DISC)
    lst = game_stop_parse(
        BeautifulSoup(website.content, 'html.parser'), GAMESTOP_URL_DISC
    )
    lst.append("DISC")

    data.append(lst)

    website = requests.get(GAMESTOP_URL_DIGI)
    lst = game_stop_parse(BeautifulSoup(website.content, 'html.parser'),
                          GAMESTOP_URL_DIGI)
    lst.append("DIGI")
    data.append(lst)

    website = requests.get(AMAZON_URL_DISC)
    lst = amazon(BeautifulSoup(website.content, 'html.parser'),
                 AMAZON_URL_DISC)
    lst.append("DISC")
    data.append(lst)

    website = requests.get(AMAZON_URL_DIGI)
    lst = amazon(BeautifulSoup(website.content, 'html.parser'),
                 AMAZON_URL_DIGI)
    lst.append("DIGI")
    data.append(lst)

    website = requests.get(SONY_URL_DISC)
    lst = sony(BeautifulSoup(website.content, 'html.parser'),
               SONY_URL_DISC)
    lst.append("DISC")
    data.append(lst)

    website = requests.get(SONY_URL_DIGI)
    lst = sony(BeautifulSoup(website.content, 'html.parser'),
               SONY_URL_DISC)
    lst.append("DIGI")
    data.append(lst)

    website = requests.get(CANADACOMP_URL)
    lst = canada_computers_parse(BeautifulSoup(website.content, 'html.parser'),
                                 CANADACOMP_URL)
    lst.append("DISC")
    data.append(lst)

    # print(data)

    f = open("data.txt", "w")

    for line in data:
        trimmed = str(line)[2:-2]
        f.write(trimmed)
        f.write("\n")
    f.close()


main()
