import difflib
import csv
from math import sqrt

from redisdb.database import redis_execute, get_pipeline


pipe = get_pipeline()


class PR():

    def __init__(self):
        pass

    @staticmethod
    def get_user_commit_info(user_name):
        count = 0
        redis_execute(pipe, "hkeys", "user")
        user_list = pipe.execute()[0]
        for user in user_list:
            # similar user name handle
            seq = difflib.SequenceMatcher(None, user.lower(), user_name.lower())
            if seq.ratio() > 0.8:
                redis_execute(pipe, "hget", "user", user)
        result = pipe.execute()
        for res in result:
            if res != "True":
                count += int(res)
        return {"name": user_name, "count": count}


    @staticmethod
    def get_info_from_csv(result, user_name):
        f = open("data.csv", 'rb')
        try:
            reader = csv.reader(f)
            for user_id, name, dev, new, pic_url in reader:
                seq = difflib.SequenceMatcher(None, name.lower(), user_name.lower())
                if seq.ratio() > 0.8:
                    result = {
                        "id": int(user_id),
                        "name": name,
                        "dev": int(dev),
                        "new": int(new),
                        "pic_url": pic_url
                    }
        finally:
            f.close()
        return result

    @staticmethod
    def get_info_from_csv(self, result):
        f = open("data.csv", 'rb')
        try:
            reader = csv.reader(f)
            for user_id, name, dev, new, pic_url, commit_name, expr, tw_expr in reader:
                commit = self.get_user_commit_info(commit_name)
                year_story = 160
                if int(new) == 0:
                    point = int(commit["count"]) * sqrt(float(expr))
                else:
                    point = year_story * sqrt(float(expr)) * int(commit["count"]) / year_story

                result.append({
                    "id": int(user_id),
                    "name": name,
                    "dev": int(dev),
                    "new": int(new),
                    "pic_url": pic_url,
                    "point": commit,
                    "expr": float(expr),
                    "expr_tw": float(tw_expr),
                    "pr": int(point)
                })
        finally:
            f.close()
        return result