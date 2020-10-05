from functools import lru_cache

def auto_correct(cities_list, city):
    """Uses minimum_edit_distance to determine the closest-resembling
    city in CITIES_LIST to CITY.
    """
    city = city.title()

    if city not in cities_list:
        reference = reformat(city)
        curr_min, curr_city = float('inf'), None

        for c in cities_list:
            word = reformat(c)
            d = minimum_edit_distance(reference, word)

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

def reformat(s):
    """Reformats a string S for comparison.
    """

    return ''.join(s.split(' ')).lower()