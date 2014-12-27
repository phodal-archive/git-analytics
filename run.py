from datetime import datetime
from pandas import date_range
import shlex
import subprocess as sp
import sys, string, re

start = datetime(year=2014, month=12, day=01)
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
    text = ""
    for messages in get_all_commit_message(date_range):
        for msg in messages:
            text += msg
    return text

text = get_pure_text_message(range)