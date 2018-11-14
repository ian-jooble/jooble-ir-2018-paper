# PAPER search engine

### Table of contents:
- Services description
- Index realization
- Testing
- Data
- TODO

## Services:

Services filenames ends with last 2 digits of port number to call it (search_68 - port 13568)
> Ports will be later in config file

### search_68
Search server provide **UI hosting** and **all search workflow**

Receive: ajax post request from user interface with meta and search<br>
Return: ranked docs

Make call to:
- Analyzer service (analyzer_71) with user search query and receive stemmed tokenized query and lang
- Rank service (rank_70) with preprocessed query

### analyzer_71
Analyzer provide **stemm, tokenize and lang detect** workflow
    
Receive: list of lists of textes<br>
Return: list of lists of stemmed tokens for each document & list of languages codes

Make call to:
- Language detection service (lang_detection_67) with query
- Stemmer service (stemmer_66) with query

### stemmer_66
Provide stemming and tokenization

Receive: text document and language<br>
Return: list of stemmed tokens for document

### lang_detection_67
Make language detection of texts list

Receive: list of strs<br>
Returns: list of detected languages (strs code like de, en etc.)

### rank_70
Make search in index and rank documents using paper.index module

Receive: list of meta, stemmed_query<br>
Return: list of ranked documents

### updater_72
Make index update using paper.index module

Receive: textes - list of strs<br>
Return: list of ids of updated documents

Make call to:
- Analyzer service with textes


## Index
Index is a Redis database

There is module paper.index where basic functions for working with index are provided:

Function | Arguments | Description
------------ | ------------- | --------
`update_index(docs, stemmed)` | **docs** - list or array of strs <br> **stemmed** - list of lists with token strs | Make indexing of textes (inverted and forward)<br>Return: list of ids of updated docs
`from_eval_texts(path='../../Data/eval_texts.csv')`| **path** - path to eval_textes.csv | Make update from eval textes<br>Return: list of ids of updated docs
`search(tokens)` | **tokens** - stemmed tokens for search  | Make search (boolean AND - intersect of sets)<br>Return: returns set of doc_ids strs (like "23" or "12345")
`get_docs(ids, is_str=False)` | **ids** - int ids of docs if **is_str=False**,<br>in other case: **ids** - strs of ids like 'doc:id' | Get docs by their ids<br>Returns: list of strs (documents textes)

## Testing
There is a folder **testing** where are some notebooks for testing apis (lang_detect, update)

## Data
Data folder consist eval_textes.csv and hhru.json (parsed vacancies from hh.ru)

# TODO
- [ ] Make doc class
- [ ] Snippets api
- [ ] Make other functions for index like delete(ids) etc.
- [ ] Make doc as a HASH instance in redis database
- [ ] Config file for ports and other stuff
- [ ] Config for redis db
- [ ] Make Stemmer for other languages
- [ ] Make function to create Index from parsed data from hh.ru