from flask import Flask
from flask.ext import restful
from flask.ext.cache import Cache

from run import Info
from pr import PR

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

api = restful.Api(app)
info = Info()
pr = PR()
all_info = pr.get_info_from_csv(pr, [])


class User(restful.Resource):
    @staticmethod
    def get(user_name):
        information = pr.get_user_commit_info(pr, user_name)
        return information, 201


class UserInfo(restful.Resource):
    @staticmethod
    def get(user_name):
        result = []
        result = pr.get_info_from_csv(result, user_name)
        result["more"] = pr.get_user_commit_info(user_name)
        return result, 201


class All(restful.Resource):
    @staticmethod
    def get():
        return all_info, 201, {'Access-Control-Allow-Origin': '*'}


api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserInfo, '/userInfo/<string:user_name>')
api.add_resource(All, '/all/account')

if __name__ == '__main__':
    app.run(debug=True)