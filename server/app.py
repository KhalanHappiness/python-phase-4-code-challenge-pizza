#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False


CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants (Resource):

    def get(self):

        restaurants = Restaurant.query.all()

        resaurant_dict = [restaurant.to_dict(rules = ("-restaurant_pizzas",)) for restaurant in restaurants]

        response = make_response(
            resaurant_dict,
            200
        )

        return response
    
class RestaurantsById(Resource):

    def get(self, id):

        restaurant = Restaurant.query.filter(Restaurant.id == id ).first()

        

        if restaurant:

            restaurant_dict = restaurant.to_dict()
            response = make_response(
                restaurant_dict,
                200
            )

            return response
        
        else:

            return make_response(
                {"error":"Restaurant not found"},
                404)
        
    def delete(self, id):
        restaurant = Restaurant.query.get(id)

        if restaurant is None:
            return make_response(
                {"error": "Restaurant not found"}, 
                404)
        db.session.delete(restaurant)
        db.session.commit()
        
        return '', 204
    
class Pizzas(Resource):
   

        def get(self):

            pizzas = Pizza.query.all()

            pizza_dict = [pizza.to_dict(rules = ("-restaurant_pizzas",)) for pizza in pizzas]

            response = make_response(
                pizza_dict,
                200
            )

            return response
        
class RestaurantPizzas(Resource):

    def post(self):
        try:
            data = request.get_json()
            
            # Create new RestaurantPizza
            restaurant_pizza = RestaurantPizza(
                price=data.get('price'),
                pizza_id=data.get('pizza_id'),
                restaurant_id=data.get('restaurant_id')
            )
            
            db.session.add(restaurant_pizza)
            db.session.commit()
            
            # Return the created RestaurantPizza with related data
            return restaurant_pizza.to_dict(), 201
            
        except ValueError as e:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400
        except Exception as e:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400

        

    
api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantsById, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')





if __name__ == "__main__":
    app.run(port=5555, debug=True)
