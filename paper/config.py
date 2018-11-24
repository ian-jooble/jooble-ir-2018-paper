"""
Config file class for all services
"""
import os


base_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[:-1][0]
data_dir = os.path.join(base_dir, 'Data')
by_dir = os.path.join(data_dir, 'by')

SEARCH_PORT = 13568
RANK_PORT = 13570
STEMMER_PORT = 13566
UPDATER_PORT = 13572
ANALYZER_PORT = 13571
LANGDETECT_PORT = 13567

ANALYZER_QUERY_PORT = 13573

SEARCH_PATH = "/search"
RANK_PATH = "/rank"
STEMMER_PATH = "/stemmer"
UPDATER_PATH = "/update"
ANALYZER_PATH = "/analyze"
LANGDETECT_PATH = "/lang_detect"

ANALYZER_QUERY_PATH = "/analyze"