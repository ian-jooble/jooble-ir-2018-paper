import re

from langdetect import detect
import nltk


stemmer_ru = nltk.stem.snowball.RussianStemmer()
stemmer_en = nltk.stem.porter.PorterStemmer()


def normalize(s):
    s = s.lower()
    # Isolate punctuation
    s = re.sub(r'([\'\"\.\(\)\!\?\\\\,\·])', r' \1 ', s)
    # Remove some special characters
    s = re.sub(r'([\;\:\|•«»\n()·,.""~`()!?-])', '', s)
    s = s.replace('\xa0', ' ')
    s = s.replace('\r', ' ')
    s = s.replace('\n', ' ')
    s = s.replace('©', ' ')
    return s


def normalized_and_stemmed(s):
    s = normalize(s)
    
    lang = detect(s)
    if lang=='en':
        s = [stemmer_en.stem(tok) for tok in s.split()]
    else:
        s = [stemmer_ru.stem(tok) for tok in s.split()]
    return ' '.join(s)