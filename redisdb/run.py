import nltk
from nltk.collocations import *

from redisdb.commits import Commit


bigram_measures = nltk.collocations.BigramAssocMeasures()
commit = Commit()
finder = BigramCollocationFinder.from_words(commit.get())
finder.nbest(bigram_measures.pmi, 100)


class Info:
    def __init__(self):
        pass

    @staticmethod
    def bigrams():
        print finder.nbest(bigram_measures.pmi, 100)
        return finder.nbest(bigram_measures.pmi, 100)