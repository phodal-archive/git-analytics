from flask import Flask, flash
from flask.ext import restful
from flask_restful import reqparse, Resource

from flask.ext.cache import Cache
from run import Info
from pr import PR
from db import get_db


app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

api = restful.Api(app)
info = Info()
pr = PR()
all_info = pr.get_info_from_csv(pr, [])


class User(Resource):
    @staticmethod
    def get(user_name):
        information = pr.get_user_commit_info(pr, user_name)
        return information, 201


class UserInfo(Resource):
    @staticmethod
    def get(user_name):
        result = []
        result = pr.get_info_from_csv(result, user_name)
        result["more"] = pr.get_user_commit_info(user_name)
        return result, 201


class All(Resource):
    @staticmethod
    def get():
        return all_info, 201, {'Access-Control-Allow-Origin': '*'}


parser = reqparse.RequestParser()
parser.add_argument('user', type=str)
parser.add_argument('story_number', type=str)
parser.add_argument('story_type', type=str)
parser.add_argument('story_title', type=str)
parser.add_argument('story_day', type=int)
parser.add_argument('story_description', type=str)


class Story(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        db = get_db()
        db.execute(
            'insert into pair (story_type, story_number, story_description, story_title, user, story_day) values (?, ?, ?, ?, ?, ?)',
            [args["story_type"], args["story_number"], args["story_description"], args["story_title"], args["user"],
             args["story_day"]])
        db.commit()
        flash('New entry was successfully posted')
        return args, 201

    @staticmethod
    def get():
        db = get_db()
        results = []
        cursor = db.execute('select * from pair')
        for information in cursor.fetchall():
            result = {"story_type": information["story_type"],
                      "story_number": information["story_number"],
                      "story_description": information["story_description"],
                      "story_title": information["story_title"],
                      "user": information["user"],
                      "story_day": information["story_day"]}
            results.append(result)
        db.commit()
        return results, 201


api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserInfo, '/userInfo/<string:user_name>')
api.add_resource(All, '/all/account')
api.add_resource(Story, '/story')

if __name__ == '__main__':
    app.run(debug=True)