import nltk
from nltk.collocations import *
from commits import Commit
import json

bigram_measures = nltk.collocations.BigramAssocMeasures()

commit = Commit()
finder = BigramCollocationFinder.from_words(commit.get())

# only bigrams that appear 3+ times

# return the 5 n-grams with the highest PMI
finder.nbest(bigram_measures.pmi, 100)

class Info:
    def __init__(self):
        pass

    def bigrams(self):
        print finder.nbest(bigram_measures.pmi, 100)
        return  finder.nbest(bigram_measures.pmi, 100)