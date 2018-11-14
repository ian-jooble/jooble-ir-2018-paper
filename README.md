# jooble-ir-2018-paper


search_server_68.ipynb creates web-page, get a query from it and send it to index_server_69.ipynb.

index_server_69.ipynb are using for searching for docIDs in the inverted index and updating forward index and inverted index

database_preprocessing.ipynb preprocess hhru.json, crawled information about vacancies from hh.ru, and update it in our db

Our database is Redis, it helps us with asynchronous requests

/paper contains functions for inverted and forward indexes

/templates contains files for the web-page with a search form. 

/in_progress contains unfinished files
