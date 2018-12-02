import re

from langdetect import detect
import nltk


stemmer_ru = nltk.stem.snowball.RussianStemmer()
stemmer_en = nltk.stem.porter.PorterStemmer()


def detect_lang(s):
    """
    Detect lang of s
    Use it in lang detection server
    """
    return detect(s)


def normalize(s):
    s = s.lower()
    s = s.replace('\xa0', ' ')
    s = s.replace('\r', ' ')
    s = s.replace('\n', ' ')
    s = s.replace('©', ' ')  
    # Isolate punctuation
    # s = re.sub(r'([\'\"\.\(\)\!\?\\\\/\,\·])', r' \1 ', s)
    # Remove some special characters
    s = re.sub(r'([\;\:\|•«»\n()·,.""~`()!?])', '', s)
    s = s.replace('/', ' ')
    s = s.replace('-', ' ')
    s = s.replace('%', ' ')
    s = s.replace('*', ' ')
    return s


def normalize_and_stemm(s, lang):
    """
    Normalize and stemm s
    Use it in stemmer service
    Recive s str and lang str
    Returns list of stemmed tokens
    """
    s = normalize(s)
    
    if lang=='en':
        s = [stemmer_en.stem(tok) for tok in s.split()]
    else:
        s = [stemmer_ru.stem(tok) for tok in s.split()]
    return s


def norm_stem_lang(s):
    """
    do all workflow for analyzer
    do not use in prodaction
    """
    lang = detect_lang(s)
    return normalize_and_stemm(s, lang)