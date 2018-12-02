"""
Module for handling with index database
"""
from redis import Redis
import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer


redis_conn = Redis(decode_responses=True)


def update_index(docs):

    pipe = redis_conn.pipeline()

    max_id = redis_conn.get("max doc id")
    if max_id is None:
        max_id = 0
    else:
        max_id = int(max_id)
    new_ids = range(max_id, len(docs), 1)

    for doc, stm_doc, doc_id in zip(docs, stemmed, new_ids):
        #  update index
        pipe.hmset("inv doc:{}".format(doc_id), doc)
        #  update inverted index
        for tok in stm_doc:
            pipe.sadd("inv+ "+tok, doc_id)

    max_id += len(docs)
    pipe.execute()


def update_tfidf(docs, stemmed):
    """
    docs - list of dicts
    stemmed - list of stemmed textes
    returns list of ids of updated docs
    """
    max_id = redis_conn.get("max doc id")
    if max_id is None:
        max_id = 0
    else:
        max_id = int(max_id)
    new_ids = list(range(max_id, len(docs), 1))
    
    pipe = redis_conn.pipeline()
    tf_idf_vectorizer = TfidfVectorizer()
    X = tf_idf_vectorizer.fit_transform(stemmed)
    vocab = tf_idf_vectorizer.vocabulary_
    inv_vocab = {vocab[key]: key for key in vocab}

    cx = scipy.sparse.coo_matrix(X)

    for d_id, tok_id, tf_idf in zip(cx.row, cx.col, cx.data):
        pipe.zadd(inv_vocab[tok_id], d_id, tf_idf)
    pipe.execute()

    for new_doc, new_id in zip(docs, new_ids):
        pipe.hmset("doc:{}".format(new_id), new_doc)
    pipe.incrby("max doc id", len(docs))
    # print(pipe.execute())
    return list(new_ids)


def search_tfidf(tokens, limit=-1):
    """
    tokens - list of strs
    returns list with tuples (doc_id, score)
    """
    if len(tokens) == 1:
        ids = redis_conn.zrange(tokens[0], 0, limit,
                                withscores=True,
                                score_cast_func=float)
    else:
        # maybe we already have that query in cache
        stemmed_query = ' '.join(tokens)
        ids = redis_conn.zrange(stemmed_query, 0, limit,
                                withscores=True,
                                score_cast_func=float)
        # if not - make a cache with 90 sec expire time
        if len(ids) == 0:
            pipe = redis_conn.pipeline()
            pipe.zinterstore(stemmed_query, tokens, )
            pipe.zrange(stemmed_query, 0, limit,
                        withscores=True,
                        score_cast_func=float)
            ids = pipe.execute()[-1]
            redis_conn.expire(stemmed_query, 30)
    return ids[::-1]


def search(tokens):
    """
    Function is deprecated, do not use
    """
    tokens = ["inv+ "+tok for tok in tokens]
    ids = redis_conn.sinter(*tokens)
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
    Delete redis db
    """
    redis_conn.flushall()
