import json
from flask import Flask
from flask.ext import restful
from run import Info
from database import redis_execute, get_pipeline

app = Flask(__name__)
api = restful.Api(app)
pipe = get_pipeline()

info = Info()


class HelloWorld(restful.Resource):
    def get(self):
        return info.bigrams()


class User(restful.Resource):
    def get(self, user_name):
        redis_execute(pipe, "hget", "user", user_name)
        result = pipe.execute()
        return {"count": result[0]}, 201


api.add_resource(HelloWorld, '/')
api.add_resource(User, '/user/<string:user_name>')

if __name__ == '__main__':
    app.run(debug=True)