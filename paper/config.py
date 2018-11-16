"""
Config file class for all services
"""
import os


base_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[:-1]

SEARCH_PORT = 13568
RANK_PORT = 13570
STEMMER_PORT = 13566
UPDATER_PORT = 13572
ANALYZER_PORT = 13571
LANGDETECT_PORT = 13567

SEARCH_PATH = "/search"
RANK_PATH = "/rank"
STEMMER_PATH = "/stemmer"
UPDATER_PATH = "/update"
ANALYZER_PATH = "/analyze"
LANGDETECT_PATH = "/lang_detect"
