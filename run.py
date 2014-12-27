from datetime import datetime
from pandas import date_range
import shlex
import subprocess as sp

start = datetime(year=2010, month=10, day=24)
end = datetime.today()
rng = date_range(start, end, freq='W')

cmd = 'git log --oneline --since=%s --until=%s --no-merges'


def commit_message(since_data, util_date):
    p = sp.Popen(shlex.split(cmd % (since_data, util_date)), stdout=sp.PIPE)
    p.wait()
    return p.stdout.readlines()


def get_all_commit_message(date_range):
    commit_messages = []
    for idx in xrange(len(date_range) - 1):
        since_date = date_range[idx]
        since_iso = since_date.date().isoformat()
        until_iso = date_range[idx + 1].date().isoformat()
        commit_messages.append((since_date, commit_message(since_iso, until_iso)))
    return commit_messages


print get_all_commit_message(rng)