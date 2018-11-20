"""
Module for handling with index database
"""

from redis import Redis
import pandas as pd


redis_conn = Redis(decode_responses=True)


def update_index(docs, stemmed):
    """
    docs - list or array of strs
    stemmed - list of lists with token strs
    returns list of ids of updated docs
    """

    pipe = redis_conn.pipeline()

    max_id = pipe.get("max doc id").execute()[0]
    if max_id is None:
        max_id = 0
    else:
        max_id = int(max_id)

    new_ids = range(max_id, len(docs), 1)

    for doc, stm_doc, doc_id in zip(docs, stemmed, new_ids):
        #  update index
        #  TODO: make doc great again! (as a HASH object)
        pipe.set("doc:{}".format(doc_id), doc)
        #  update inverted index
        for tok in stm_doc:
            pipe.sadd(tok, doc_id)
    pipe.incrby("max doc id", len(docs))
    pipe.execute()
    return list(new_ids)


def from_eval_texts(path='./Data/eval_texts.csv'):
    """
    Method for hydrating index from dump csv data
    './Data/eval_texts.csv' - using in services
    """
    df = pd.read_csv(path, sep='\t')
    documents = df.text.values[:100]
    documents_stemmed = df.text_searchable.values[:100]
    stemmed = [s_doc.split() for s_doc in documents_stemmed]
    return update_index(documents, stemmed)


def search(tokens):
    """
    tokens - list of strs
    returns set of doc_ids strs
    """
    pipe = redis_conn.pipeline()
    ids = pipe.sinter(*tokens).execute()[0]
    return ids


def get_docs(ids, is_str=False):
    """
    ids - list of ids (integers or strings like "doc:<id>")
    returns list of strs
    """
    pipe = redis_conn.pipeline()
    if is_str:
        for doc_id in ids:
            pipe.get(doc_id)
    else:
        for doc_id in ids:
            pipe.get("doc:{}".format(doc_id))
    return pipe.execute()
