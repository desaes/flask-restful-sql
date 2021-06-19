from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'  # this key should be keep out of code
api = Api(app)

jwt = JWT(app, authenticate, identity) # JWT creates a new /auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot bet left blank!"
    )    

    @jwt_required()
    def get(self, name):
        # Filter returns a filter object and you have some functions to manipulate it like list, next
        # item = list(filter(lambda x: x['name'] == name, items)) # if filter returns a list
        item = next(filter(lambda x: x['name'] == name, items), None) # first item found by filter function. Can be called multiple times.
        # Above, if filter returns None, an error will be triggered. So, define None as default value of next
        return {'item': item}, 200 if item else 404 # ok -> 200 || not found -> 404

    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exist.".format(name)}, 400 # bad request -> 400

        request_data = Item.parser.parse_args()
        #request_data = request.get_json(force=true) # if content type is not setted to json, it forces the parsing, not recomended
        #request_data = request.get_json(silent=True) # basically return none if content type is not setted to json
 
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201 # created -> 201
                         # accepted -> 202, used when queueing operations0

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        #request_data = request.get_json(silent=True) # basically return none if content type is not setted to json
        request_data = Item.parser.parse_args()
        
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item, 201
        

class ItemList(Resource):
    def get(self):
        return {'items': items}

        

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug=True)
