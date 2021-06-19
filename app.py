from flask import Flask,jsonify
from flask_restful import Api

from flask_jwt import JWT
from security import authenticate, identity

from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'jose'  # this key should be keep out of code
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login' # will change the default /auth to /login
# config JWT to expire within half an hour
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWT(app, authenticate, identity) # JWT creates a new /auth

# customize JWT auth response, include user_id in response body
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#    return jsonify({
#                        'access_token': access_token.decode('utf-8'),
#                        'user_id': identity.id
#                   })

# @jwt.error_handler
# def customized_error_handler(error):
#    return jsonify({
#                       'message': error.description,
#                       'code': error.status_code
#                   }), error.status_code

# for more
# https://blog.teclado.com/learn-python-advanced-configuration-of-flask-jwt/
# https://pythonhosted.org/Flask-JWT/

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
