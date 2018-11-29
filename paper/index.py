"""
Module for handling with index database
"""
from redis import Redis
from collections import Counter
from math import log


redis_conn = Redis(decode_responses=True)
# constant for tf-idf
N = 10e9


def update_index(docs, stemmed):
    """
    docs - list of dicts
    stemmed - list of lists with token strs
    returns list of ids of updated docs
    """

    pipe = redis_conn.pipeline()

    max_id = redis_conn.get("max doc id")
    if max_id is None:
        max_id = 0
    else:
        max_id = int(max_id)
    new_ids = range(max_id, len(docs), 1)

    vocabulary = set(sum(stemmed, []))

    #  calculate document frequency for each token
    #  local_df - {token: df}
    local_df = {}
    for stm_doc in stemmed:
        for tok in vocabulary:
            if tok in stm_doc:
                try:
                    local_df[tok] += 1
                except KeyError:
                    local_df[tok] = 1

    #  local_tf_dict - {doc_id: {token: tf}}
    #  tf for new documents
    local_tf_dict = {}
    for doc, stm_doc, doc_id in zip(docs, stemmed, new_ids):
        local_tf_dict[doc_id] = Counter(stm_doc)

    #  inverted index for new documents
    #  invindex - {tok: {doc_id, ...} }
    texts = {i: stem for i, stem in zip(new_ids, stemmed)}
    invindex = {word: set(txt for txt, wrds in texts.items() if word in wrds)
                for word in vocabulary}

    routine_pipe = redis_conn.pipeline()  # make pipeline for routine tasks
    #  existingt tf-idf for each token in vocabulary to change
    #  { tok: [(doc_id, tfidf)], .. }
    for tok in vocabulary:
        routine_pipe.zrange(tok, 0, -1, withscores=True, score_cast_func=float)
    buff = routine_pipe.execute()
    old_table_vocab = {tok: lst for tok, lst in zip(vocabulary, buff)}

    # get old df from redis
    # old_df_dict - {tok: df} (df - len of docs in redis for token tok)
    for tok in vocabulary:
        routine_pipe.zcount(tok, '-inf', '+inf')
    buff = routine_pipe.execute()
    old_df_dict = {tok: df for tok, df in zip(vocabulary, buff)}

    #  now we can iterate througth new vocabulary and docs to
    #  calculate new tf-idf
    new_index = {}
    for tok in vocabulary:
        new_index[tok] = {}

        loc_df = local_df[tok]
        old_df = old_df_dict[tok]
        new_df = loc_df + old_df   # count of all docs with token tok
        loc_post_list = invindex[tok]   # set of new doc ids where tok is
        old_tfidf_tuples = old_table_vocab[tok]   # list with pairs (old_doc_id, tf-idf)

        #  calculate tf_idf for new docs and vocab
        for new_doc_id in loc_post_list:
            tf = local_tf_dict[new_doc_id][tok]
            new_tfidf = (1 + log(tf, 10)) * log(N/loc_df, 10)
#             print('-'*40, '\ntok = ', tok, '\ntf = ', tf,
#                   '\n0ld_df = ', old_df, '\ntfidf = ', new_tfidf,
#                   '\nloc_df = ', loc_df,
#                   '\nnew_doc_id =', new_doc_id)
            new_index[tok][new_doc_id] = new_tfidf

        #  recalculate tf_idf for existing docs in redis
        for old_doc_id, old_tf_idf in old_tfidf_tuples:
            new_tfidf = old_tf_idf * log(N/new_df, 10) / log(N/old_df, 10)
#             print('+'*40, '\ntok = ', tok,
#                   '\n0ld_df = ', old_df, '\ntfidf = ', new_tfidf,
#                   '\nold_tfidf = ', old_tf_idf,
#                   '\nloc_df = ', loc_df,
#                   '\nold_doc_id =', old_doc_id)
            new_index[tok][old_doc_id] = new_tfidf

        [pipe.zadd(tok, d_id, new_index[tok][d_id]) for d_id in new_index[tok].keys()]
        pipe.execute()

    for new_doc, new_id in zip(docs, new_ids):
        pipe.hmset("doc:{}".format(new_id), new_doc)
    pipe.incrby("max doc id", len(docs))
    print(pipe.execute())
    return list(new_ids)


def search(tokens):
    """
    tokens - list of strs
    returns list with tuples (doc_id, score)
    """
    if len(tokens) == 1:
        print('just 1 token')
        ids = redis_conn.zrange(tokens[0], 0, 1,
                                withscores=True,
                                score_cast_func=float)
    else:
        # maybe we already have that query in cache

        stemmed_query = ' '.join(tokens)
        ids = redis_conn.zrange(stemmed_query, 0, 1,
                                withscores=True,
                                score_cast_func=float)
        # if not - make a cache with 90 sec expire time
        if len(ids) == 0:
            print('do no use chahe')
            pipe = redis_conn.pipeline()
            pipe.zinterstore(stemmed_query, tokens, )
            pipe.zrange(stemmed_query, 0, -1,
                        withscores=True,
                        score_cast_func=float)
            ids = pipe.execute()[-1]
            redis_conn.expire(stemmed_query, 90)
        else:
            print('using chache')
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
