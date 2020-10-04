import pandas as pd
from functools import lru_cache

# Basic formatting
cities = pd.read_csv('worldcities.csv', sep=',')

def auto_correct(city):
    cities_list = list(cities['city'])
    if city not in cities_list:
        ref = ''.join(city.split(' ')).lower()
        curr_min, curr_city = float('inf'), None
        for c in cities_list:
            word = ''.join(c.split(' ')).lower()
            d = minimum_edit_distance(ref, word)
            if d < curr_min:
                curr_min = d
                curr_city = c
        city = curr_city
    return city

@lru_cache(maxsize=None)
def minimum_edit_distance(reference, word):
    """Compares a WORD to REFERENCE and quantifies how closesly
    they resemble one another.
    """

    if not reference or not word:
        return len(reference) or len(word)
    else:
        add = 1 + minimum_edit_distance(reference[1:], word)
        rem = 1 + minimum_edit_distance(reference, word[1:])
        sub = (reference[0] != word[0]) + minimum_edit_distance(reference[1:], word[1:])

        return min(add, rem, sub)