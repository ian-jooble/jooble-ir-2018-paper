"""
Module for handling with index database
"""

from redis import Redis
import pandas as pd


redis_conn = Redis(decode_responses=True)


def update_index(docs, stemmed):
    """
    docs - list of dicts
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
        doc['stemmed'] = stm_doc
        pipe.hmset("doc:{}".format(doc_id), doc)
        #  update inverted index
        for tok in stm_doc:
            tf = stm_doc.count(tok)
            pipe.zadd(tok, tf, doc_id)
            
    pipe.incrby("max doc id", len(docs))
    pipe.execute()
    return list(new_ids)


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
            pipe.hgetall(doc_id)
    else:
        for doc_id in ids:
            pipe.hgetall("doc:{}".format(doc_id))
    return pipe.execute()


def delete_all():
    """
    Delete all data from db
    """
    redis_conn.flushall()