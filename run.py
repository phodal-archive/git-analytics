from datetime import datetime
import shlex
import subprocess as sp

from pandas import date_range

from gitinspector import changes


start = datetime(year=2012, month=12, day=01)
end = datetime.today()
range = date_range(start, end, freq='W')

cmd = "git log --oneline --since=%s --until=%s --no-merges --pretty=format:'%s'"


def commit_message(since_data, util_date):
    p = sp.Popen(shlex.split(cmd % (since_data, util_date, '%s')), stdout=sp.PIPE)
    p.wait()
    return p.stdout.readlines()


def get_all_commit_message(date_range):
    commit_messages = []
    for index in xrange(len(date_range) - 1):
        since_date = date_range[index]
        since_iso = since_date.date().isoformat()
        until_iso = date_range[index + 1].date().isoformat()
        commit_messages.append((commit_message(since_iso, until_iso)))
    return commit_messages


def get_pure_text_message(date_range):
    results = ""
    for messages in get_all_commit_message(date_range):
        for msg in messages:
            if "CSBAU" in msg or "CASAXIAN" in msg:
                msg = msg.replace(":", "")
                msg = msg.replace("&", "")
                results += msg

    return results


text = get_pure_text_message(range).split()

print text

import nltk
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()

finder = BigramCollocationFinder.from_words(text)

# only bigrams that appear 3+ times
finder.apply_freq_filter(1)

print ""
# return the 5 n-grams with the highest PMI
print finder.nbest(bigram_measures.pmi, 100)

hard = False
authorinfo_list = changes.get(hard).get_authorinfo_list()
for i in authorinfo_list:
    print authorinfo_list.get(i).commits