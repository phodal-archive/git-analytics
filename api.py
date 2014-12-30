from flask import Flask
from flask.ext import restful
from run import Info
import difflib
from database import redis_execute, get_pipeline


app = Flask(__name__)
api = restful.Api(app)
pipe = get_pipeline()

info = Info()


class HelloWorld(restful.Resource):
    @staticmethod
    def get():
        return info.bigrams()


class User(restful.Resource):
    @staticmethod
    def get(user_name):
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
        return {"name": user_name, "count": count}, 201


api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user/<string:user_name>')

if __name__ == '__main__':
    app.run(debug=True)