import nltk
from nltk.collocations import *
from gitinspector import changes
from commits import Commit

bigram_measures = nltk.collocations.BigramAssocMeasures()

commit = Commit()
finder = BigramCollocationFinder.from_words(commit.get())

# only bigrams that appear 3+ times
finder.apply_freq_filter(1)

print ""
# return the 5 n-grams with the highest PMI
print finder.nbest(bigram_measures.pmi, 100)

hard = False
authorinfo_list = changes.get(hard).get_authorinfo_list()
for i in authorinfo_list:
    print authorinfo_list.get(i).commits