import requests
from time import sleep


def get_text(query):
    tries = 10
    while tries > 0:
        try:
            text = requests.get(query).text
            return text
        except:
            tries -= 1
            sleep(1)
