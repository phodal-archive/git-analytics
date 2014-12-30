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
                print res
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
            for name, dev, new, pic_url in reader:
                seq = difflib.SequenceMatcher(None, name.lower(), user_name.lower())
                if seq.ratio() > 0.8:
                    result = {
                        "name": name,
                        "dev": dev,
                        "new": new,
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


api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserInfo, '/userInfo/<string:user_name>')

if __name__ == '__main__':
    app.run(debug=True)