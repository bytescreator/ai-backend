import logging
import os
import sys
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


def mk_header(link: str):
    return {
        "Accept": "text/html, */*; q = 0.01",
        "Accept-Language": "en-US, en;q = 0.5",
        # Cookie
        # userID = 38e2a9ea-cb71-4cdd-8b3a-3f846cff1631
        # _ga_WGBDLK44E4 = GS1.1.1735389115.6.1.1735389170.5.0.0
        # _ga = GA1.1.249052878.1733930664
        # _gcl_au = 1.1.1448579182.1733930669
        # nyt_web_push_maybe_later_v2 = 1
        # app_presentation_never_show_again = 1
        "Host": "www.nefisyemektarifleri.com",
        "Referer": link,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "X-Requested-With": "XMLHttpRequest",
    }


def invokable_search_meal_recipes(query: str, page: int):
    """
    this function retrieves meal recipes from nefisyemektarifleri.com. It should be the primary
    function when a meal is requested, result should be present to user with titles and
    authors, links should be hidden unless requested.
    Initial page is 1 and Gemini is expected to increase it as the user requests more recipes.

    Parameters:
    query (str): the query string to search, must be ascii.
    page (int): page number to retrieve further results, must start from 1

    Returns:
    list: list of recipes in given page, each element is a dict which contains
    the title of the recipe, link to the recipe and owner of the recipe
    """
    link = f"https://www.nefisyemektarifleri.com/ara/page/{int(page)}/"
    logging.debug(
        f"search_meal_recipes called with: {link} s={query}")
    output = []
    for card in BeautifulSoup(requests.get(link, headers=mk_header(link), params={"s": query}).content, features="html.parser").find_all(attrs={"class": "recipe-cards"}):
        header = card.h3.a
        title, link = header["title"], header["href"]
        owner = card.find(attrs={"class": "recipe-owner"})["title"]

        output.append({
            "title": title,
            "link": link,
            "owner": owner,
        })

    return output


def invokable_get_meal_recipe(link: str):
    """
    gets the detail of recipes retireved with invokable_search_meal_recipes

    Parameters:
    link (str): of the recipe

    Returns:
    str: ingredients and instructions of the recipe
    """

    logging.debug(f"invokable_get_meal_recipe called with: {link}")
    soup = BeautifulSoup(requests.get(
        link, headers=mk_header(link)).content, features="html.parser")
    print(soup, file=sys.stderr)

    return {
        "ingredients": soup.find(attrs={"class": "recipe-materials"}).text,
        "prep": soup.find(lambda tag: tag.has_attr("class") and "recipe-preparation" in tag["class"]).text
    }


def invokable_open_recipe_in_browser(link: str):
    """
    opens link in browser for recipes, should only be used with nefisyemektarifleri.com recipes

    Parameters:
    link (str): link to open

    Returns:
    bool: opened or not
    """

    os.startfile(link)
