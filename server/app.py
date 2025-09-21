#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def home():
    return "<h1>Plant Store API</h1>"

# GET /plants
@app.route("/plants", methods=["GET"])
def get_plants():
    plants = [plant.to_dict() for plant in Plant.query.all()]
    return make_response(jsonify(plants), 200)

# GET /plants/<id>
@app.route("/plants/<int:id>", methods=["GET"])
def get_plant_by_id(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)
    return make_response(jsonify(plant.to_dict()), 200)

# POST /plants
@app.route("/plants", methods=["POST"])
def create_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data.get("name"),
        image=data.get("image"),
        price=data.get("price"),
    )
    db.session.add(new_plant)
    db.session.commit()
    return make_response(jsonify(new_plant.to_dict()), 201)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
