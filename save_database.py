from database import get_pipeline, redis_execute
from commits import Commit

commit = Commit()

def save_db():
    pipe = get_pipeline()
    for messages in commit.get_all_commit_message():
        x = 1
        for msg in messages:
            print msg
            redis_execute(pipe, "zincrby", "tw", msg + "", x)
            x += 1
    pipe.execute()

print save_db()