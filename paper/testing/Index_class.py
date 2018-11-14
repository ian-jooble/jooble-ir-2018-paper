import pandas as pd


class Index:
    """
    Index class
    """
    
    def __init__(self, docs=None, stemmed=None):
        self.inv_index = {}
        self.index = {}
        self.max_id = 0
        if docs is not None and stemmed is not None:
            self.update(docs, stemmed)
       
            
    @classmethod
    def from_eval_texts(cls, path='../../Data/eval_texts.csv'):
        """
        Method for testing from dump csv data
        """
        df = pd.read_csv(path, sep='\t')
        documents = df.text.values[:10]
        documents_stemmed = df.text_searchable.values[:10]
        stemmed = [s_doc.split() for s_doc in documents_stemmed]
        return cls(documents, stemmed)
    
    
    def update(self, docs, stemmed):
        """ 
        docs - list or array of strs
        stemmed - list of lists with token strs
        returns ids of updated docs
        """
        new_ids = range(self.max_id, len(docs), 1)
        for doc, stm_doc, doc_id in zip(docs, stemmed, new_ids):
            self.index[doc_id] = doc  #  add doc to index
            for tok in stm_doc:
                try:
                    self.inv_index[tok].add(doc_id)
                except KeyError:
                    self.inv_index[tok] = set()
                    self.inv_index[tok].add(doc_id)
        self.max_id += len(docs)
        return new_ids
    
        
    def search_by_tokens(self, tokens):
        """
        tokens - list of strs
        returns set of doc_ids
        """
        sets = []
        for tok in tokens:
            sets.append(self.inv_index[tok])
        ids = set.intersection(*sets)
        return ids
    
    
    def get_docs(self, ids):
        """
        ids - iterable object of ids
        """
        return [self.index[doc_id] for doc_id in ids]