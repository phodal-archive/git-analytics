from flask import Flask
from flask.ext import restful
from run import Info

app = Flask(__name__)
api = restful.Api(app)

info = Info()

class HelloWorld(restful.Resource):
    def get(self):
        return info.bigrams()

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)