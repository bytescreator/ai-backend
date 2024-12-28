import logging
import os

import requests
from bs4 import BeautifulSoup


def contains_class(l: list[str], c: str) -> bool:
    return sum(map(lambda v: 1 if c in v else 0, l)) > 0


def filter(tag):
    return tag.has_attr("title") and (tag.has_attr("class") and (contains_class(tag["class"], "new3")) or (tag.parent.has_attr("class") and contains_class(tag.parent["class"], "new3")))


def weird_case(w: str) -> str:
    orig = "çğıöşüıÇĞİÖŞÜİ "
    trf = "cgiosucgiosui-"
    tt = str.maketrans(orig, trf)
    return w.translate(tt)


def invokable_get_general_news():
    """
    gets uncategorized news headlines and their links from haberler.com
    can be used to summarize questions like "what happened today?"

    links can be loaded by load_headline when required

    Returns:
    list: [(headlines, href)]
    """

    logging.debug(f"requested general headlines")
    return [(item['title'], item['href']) for item in BeautifulSoup(
        requests.get("https://www.haberler.com").content,
        features="html.parser").find_all(filter)
    ]


lowercase_cities = [
    "adana", "adiyaman", "afyonkarahisar", "agri", "amasya", "ankara", "antalya", "artvin",
    "aydin", "balikesir", "bilecik", "bingol", "bitlis", "bolu", "burdur", "bursa",
    "canakkale", "cankiri", "corum", "denizli", "diyarbakir", "edirne", "elazig", "erzincan",
    "erzurum", "eskisehir", "gaziantep", "giresun", "gumushane", "hakkari", "hatay", "isparta",
    "mersin", "istanbul", "izmir", "kars", "kastamonu", "kayseri", "kirkaleli", "kirsehir",
    "kocaeli", "konya", "kutahya", "malatya", "manisa", "kahramanmaras", "mardin", "mogla",
    "mus", "nevsehir", "nigde", "ordu", "rize", "sakarya", "samsun", "siirt", "sinop", "sivas",
    "tekirdag", "tokat", "trabzon", "tunceli", "sanliurfa", "usak", "van", "yozgat", "zonguldak",
    "aksaray", "bayburt", "karaman", "kirikkale", "batman", "sirnak", "bartin", "ardahan",
    "igdir", "yalova", "karabuk", "kilis", "osmaniye", "duzce"
]

category_mapping = {"3.Sayfa": "https://www.haberler.com/3-sayfa/", "Anne-Çocuk": "https://www.haberler.com/anne-cocuk/", "Burçlar": "https://www.haberler.com/burclar/", "Doğruluk Kontrolü": "https://www.haberler.com/dogruluk-kontrolu/", "Döviz Kurları": "https://www.haberler.com/doviz-kurlari/", "Dünya": "https://www.haberler.com/dunya/", "Eğitim": "https://www.haberler.com/egitim/", "Ekonomi": "https://www.haberler.com/ekonomi/", "Finans": "https://www.haberler.com/finans/", "Gamegar": "https://www.haberler.com/gamegar/", "Güncel": "https://www.haberler.com/guncel/", "Güzel Sözler": "https://www.haberler.com/guzel-sozler/", "Güzellik": "https://www.haberler.com/guzellik/", "Hava Durumu": "https://www.haberler.com/hava-durumu/", "İmsakiye": "https://www.haberler.com/imsakiye-istanbul/", "Kadın": "https://www.haberler.com/kadin/", "Komik Haberler": "https://www.haberler.com/komik-ilginc/", "Koronavirüs": "https://www.haberler.com/koronavirus/", "Kültür - Sanat": "https://www.haberler.com/kultur-sanat/", "Maç Sonuçları": "https://www.haberler.com/spor/mac-sonuclari/",
                    "Manşetler": "https://www.haberler.com/gunun-mansetleri/", "Magazin": "https://www.haberler.com/magazin/", "Moda": "https://www.haberler.com/moda/", "Namaz Vakitleri": "https://www.haberler.com/namaz-vakitleri/", "Otomobil": "https://www.haberler.com/otomobil/", "Podcast": "https://www.haberler.com/podcast/", "Politika": "https://www.haberler.com/politika/", "RSS Servisi": "https://www.haberler.com/webmasters/?sayfa=xml", "Rüya Tabirleri": "https://www.haberler.com/ruya-tabirleri/", "Sağlık": "https://www.haberler.com/saglik/", "Şans Oyunları": "https://www.haberler.com/sans-oyunlari/", "Seçim": "https://www.haberler.com/secim/", "Sitene Ekle": "https://www.haberler.com/webmasters/?sayfa=yerelhaber", "Son Dakika": "https://www.haberler.com/son-dakika/", "Son Depremler": "https://www.haberler.com/son-depremler/", "Spor": "https://www.haberler.com/spor/", "Turizm": "https://www.haberler.com/turizm/", "Teknoloji": "https://www.haberler.com/teknoloji/", "Yazarlar": "https://www.haberler.com/yazarlar/", "Yemek Tarifleri": "https://www.haberler.com/yemek-tarifi/", "Yerel Haberler": "https://www.haberler.com/yerel-haberler/"}


def invokable_get_local_news(city_name: str):
    """
    gets local news for given city name

    Parameters:
    city_name (str): city name to get news of must be one of [
        "adana", "adiyaman", "afyonkarahisar", "agri", "amasya", "ankara", "antalya", "artvin",
        "aydin", "balikesir", "bilecik", "bingol", "bitlis", "bolu", "burdur", "bursa",
        "canakkale", "cankiri", "corum", "denizli", "diyarbakir", "edirne", "elazig", "erzincan",
        "erzurum", "eskisehir", "gaziantep", "giresun", "gumushane", "hakkari", "hatay", "isparta",
        "mersin", "istanbul", "izmir", "kars", "kastamonu", "kayseri", "kirkaleli", "kirsehir",
        "kocaeli", "konya", "kutahya", "malatya", "manisa", "kahramanmaras", "mardin", "mogla",
        "mus", "nevsehir", "nigde", "ordu", "rize", "sakarya", "samsun", "siirt", "sinop", "sivas",
        "tekirdag", "tokat", "trabzon", "tunceli", "sanliurfa", "usak", "van", "yozgat", "zonguldak",
        "aksaray", "bayburt", "karaman", "kirikkale", "batman", "sirnak", "bartin", "ardahan",
        "igdir", "yalova", "karabuk", "kilis", "osmaniye", "duzce"
    ]

    Returns:
    list: [(headlines, href)]
    """
    logging.debug(f"requested local headlines : {city_name}")

    return [(item['title'], item['href']) for item in BeautifulSoup(
        requests.get("https://www.haberler.com/" +
                     city_name).content, features="html.parser"
    ).find_all(filter)]


def invokable_get_category_news(category: str):
    """
    gets news by category

    Parameters:
    category (str): must be one of ["3.Sayfa","Anne-Çocuk","Burçlar","Doğruluk Kontrolü","Döviz Kurları","Dünya","Eğitim","Ekonomi","Finans","Gamegar","Güncel","Güzel Sözler","Güzellik","Hava Durumu","İmsakiye","Kadın","Komik Haberler","Koronavirüs","Kültür - Sanat","Maç Sonuçları","Manşetler","Magazin","Moda","Namaz Vakitleri","Otomobil","Podcast","Politika","RSS Servisi","Rüya Tabirleri","Sağlık","Şans Oyunları","Seçim","Sitene Ekle","Son Dakika","Son Depremler","Spor","Turizm","Teknoloji","Yazarlar","Yemek Tarifleri","Yerel Haberler"]

    Returns:
    list: [(headlines, href)]
    """
    logging.debug(f"requested category news: {category}")
    if not category in category_mapping:
        return "unknown category"

    return [(item['title'], item['href']) for item in BeautifulSoup(
        requests.get(category_mapping[category]
                     ).content, features="html.parser"
    ).find_all(filter)]


def invokable_get_page_names(query: str):
    """
    gets category names to be used with invokable_get_direct_page

    Parameters:
    query (str): arbitrary query, should be short though.
    Returns:
    list[str]: names matched
    """
    return list(map(weird_case, [i.text for i in BeautifulSoup(requests.get(f"https://www.haberler.com/ajax/autoc.aspx?q={query}").content, features="html.parser").find_all("li")]))


def invokable_get_direct_page(name: str):
    """
    gets direct page with transformed name returned from invokable_get_page_names

    Parameters:
    name (str): query name returned by invokable_get_page_names
    Returns:
    list: [(headlines, href)]
    """
    return [(item['title'], item['href']) for item in BeautifulSoup(
        requests.get(f"https://www.haberler.com/{name}"
                     ).content, features="html.parser"
    ).find_all(filter)]


def invokable_load_headline(link: str):
    """
    gets text of the given headline link.
    This function is meant to be called when user requests more info about a headline

    Parameters:
    link (str): link to the headline specified by href

    Returns:
    str: the news content
    """
    logging.debug(f"requested headline with link : {link}")

    return BeautifulSoup(
        requests.get("https://www.haberler.com" +
                     link).content, features="html.parser"
    ).find(attrs={"id": "icerikAlani"}).text


def invokable_open_headline_in_browser(link: str):
    """
    opens given news link in users browser, should only be used with news

    Parameters:
    link (str): link to the headline

    Returns:
    bool: True if successful
    """

    os.startfile(f"https://www.haberler.com{link}")
    return True
