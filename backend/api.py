from flask import Flask
from flask_restful import Resource, Api, reqparse, request
from pymongo import MongoClient

from utils import generate_menu

app = Flask(__name__)
api = Api(app)
client = MongoClient('localhost', 27017)
db = client.menu
collection = db.menu


class Menu(Resource):
    def get(self):
        menu_list = [doc['menu'] for doc in collection.find()]
        return {"menus": sorted(menu_list)}

    def post(self):
        # sort
        parser = reqparse.RequestParser()
        parser.add_argument('menu', required=True, help="Menu name to add")
        args = parser.parse_args()
        if collection.find_one({"menu": args.menu}) is None:
            collection.insert_one({"menu": args.menu})
        return {'message': 'Menu successfully added'}

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('menu', required=True, help="Menu name to delete")
        args = parser.parse_args()
        collection.delete_one({"menu": args.menu})
        return {'message': 'Menu successfully deleted'}


class RandomMenu(Resource):
    def get(self):
        # Why reqparse not working?
        # parser = reqparse.RequestParser()
        # parser.add_argument('start_date', required=True, help="Start date to generate the random menu")
        # parser.add_argument('length', required=True, help="How many days you want to get the menus")
        # parser.add_argument('dedup_days', default=5, help="How many days you want to avoid duplication")
        # args = parser.parse_args()
        start_date = request.args.get("start_date")
        length = request.args.get("length")
        dedup_days = request.args.get("dedup_days")
        print(request.args)
        print(start_date, length, dedup_days)
        
        menu_list = [doc['menu'] for doc in collection.find()]
        try:
            return generate_menu(start_date, int(length), sorted(menu_list), int(dedup_days))
        except ValueError as e:
            return {'message': str(e)}, 400



api.add_resource(Menu, '/menu')
api.add_resource(RandomMenu, '/random_menu')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")