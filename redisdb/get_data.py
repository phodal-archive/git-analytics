import re

from redisdb.database import get_pipeline, redis_execute
from redisdb.commits import Commit


commit = Commit()


def append_message_to_database(info, msg, pipe):
    if msg.__contains__("CASAXIAN") or msg.__contains__("CSBAU"):
        redis_execute(pipe, "zincrby", "messages", msg)
        if info.__len__() is 3:
            redis_execute(pipe, "zincrby", "story", info[0].replace("[", "") , 1)
            authors = info[1].split("&")
            for author in authors:
                if 1 < author.__len__() < 20:
                    redis_execute(pipe, "hincrby", "user", author.strip())

            redis_execute(pipe, "hincrby", "message", info[2], 1)


def save_db():
    pipe = get_pipeline()
    for messages in commit.get_all_commit_message():
        for msg in messages:
            info = re.split(r'[]:]\s*', msg)
            append_message_to_database(info, msg, pipe)
    pipe.execute()

print save_db()