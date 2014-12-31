import difflib
import csv
from math import sqrt

from flask import Flask
from flask.ext import restful
from flask.ext.cache import Cache

from run import Info
from database import redis_execute, get_pipeline


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

api = restful.Api(app)
pipe = get_pipeline()

info = Info()


class User(restful.Resource):
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
    def get(user_name):
        information = User.get_user_commit_info(user_name)
        return information, 201


class UserInfo(restful.Resource):
    @staticmethod
    @cache.memoize(5000)
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
    def get(user_name):
        result = []
        result = UserInfo.get_info_from_csv(result, user_name)
        result["more"] = User.get_user_commit_info(user_name)
        return result, 201


class All(restful.Resource):
    @staticmethod
    def get():
        result = []
        result = get_info_from_csv(result)
        return result, 201, {'Access-Control-Allow-Origin': '*'}


@cache.memoize(5000)
def get_info_from_csv(result):
    f = open("data.csv", 'rb')
    try:
        reader = csv.reader(f)
        for user_id, name, dev, new, pic_url, commit_name, expr, tw_expr in reader:
            commit = User.get_user_commit_info(commit_name)
            year_story = 160
            if int(new) == 0:
                point = year_story * sqrt(float(expr))
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


api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserInfo, '/userInfo/<string:user_name>')
api.add_resource(All, '/all/account')

if __name__ == '__main__':
    app.run(debug=True)