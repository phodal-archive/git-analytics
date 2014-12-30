import difflib
import csv

from flask import Flask
from flask.ext import restful

from run import Info
from database import redis_execute, get_pipeline


app = Flask(__name__)
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
    def get_info_from_csv(result):
        f = open("data.csv", 'rb')
        try:
            reader = csv.reader(f)
            for user_id, name, dev, new, pic_url, commit_name in reader:
                commit = User.get_user_commit_info(commit_name)
                result.append({
                    "id": int(user_id),
                    "name": name,
                    "dev": int(dev),
                    "new": int(new),
                    "pic_url": pic_url,
                    "point": commit
                })
        finally:
            f.close()
        return result

    @staticmethod
    def get():
        result = []
        result = All.get_info_from_csv(result)
        return result, 201, {'Access-Control-Allow-Origin': '*'}


api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserInfo, '/userInfo/<string:user_name>')
api.add_resource(All, '/all/account')

if __name__ == '__main__':
    app.run(debug=True)