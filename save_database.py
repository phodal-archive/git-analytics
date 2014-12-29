from database import get_pipeline, redis_execute
from commits import Commit
import re

commit = Commit()

def save_db():
    pipe = get_pipeline()
    for messages in commit.get_all_commit_message():
        for msg in messages:
            info = re.split(r'[]:]\s*', msg)
            if info.__len__() is 3 and (info[0].__contains__("CASAXIAN") or info[0].__contains__("CSBAU")):
                redis_execute(pipe, "zincrby", "story", info[0].replace("[", "") + "", 1)
                authors = info[1].split("&")
                print authors
                for author in authors:
                    print author
                    redis_execute(pipe, "zincrby", "user", author + "")
                redis_execute(pipe, "zincrby", "message", info[2] + "", 1)
    pipe.execute()

print save_db()