import nltk
from nltk.collocations import *
from commits import Commit

bigram_measures = nltk.collocations.BigramAssocMeasures()

commit = Commit()
finder = BigramCollocationFinder.from_words(commit.get())

# only bigrams that appear 3+ times
finder.apply_freq_filter(1)

print commit.get_pure_text_message()
print ""
# return the 5 n-grams with the highest PMI
print finder.nbest(bigram_measures.pmi, 100)