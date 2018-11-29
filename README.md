# PAPER search engine

### Table of contents:
- Services description
- Index realization
- Testing
- Data
- TODO

## Services:

### search
Search server provide **UI hosting** and **all search workflow**

Receive: ajax post request from user interface with meta and search<br>
Return: ranked docs

Make call to:
- Analyzer service (analyzer) with user search query and receive stemmed tokenized query and lang
- Rank service (rank) with preprocessed query

### analyzer
Analyzer provide **stemm, tokenize and lang detect** workflow

Receive: list of lists of textes<br>
Return: list of lists of stemmed tokens for each document & list of languages codes

Make call to:
- Language detection service (lang_detection) with query
- Stemmer service (stemmer) with query

### stemmer
Provide stemming and tokenization

Receive: text document and language<br>
Return: list of stemmed tokens for document

### lang_detection
Make language detection of texts list

Receive: list of strs<br>
Returns: list of detected languages (strs code like de, en etc.)

### rank
Make search in index and rank documents using paper.index module

Receive: list of meta, stemmed_query<br>
Return: list of ranked documents

### updater
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
`search(tokens)` | **tokens** - stemmed tokens for search  | Make search (boolean AND - intersect of sets)<br>Return: returns set of doc_ids strs (like "23" or "12345")
`get_docs(ids, is_str=False)` | **ids** - int ids of docs if **is_str=False**,<br>in other case: **ids** - strs of ids like 'doc:id' | Get docs by their ids<br>Returns: list of strs (documents textes)
`delete_all()` | without arguments | delete all instances from redis database

## Testing
There is a folder **testing** where are some notebooks for testing apis (lang_detect, update)

## Data
Data folder consist eval_textes.csv and hhru.json (parsed vacancies from hh.ru)

# TODO
- [ ] Make doc class
- [ ] Snippets api
- [ ] Make other functions for index like delete(ids) etc.
- [x] Make doc as a HASH instance in redis database
- [x] Config file for ports and other stuff
- [ ] Config for redis db
- [ ] Make Stemmer for other languages
- [x] Make Index with `./Data/by/*` gzip files
