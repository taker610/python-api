from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lxctgcxqqgogle:d8348ea5a21e37b22d34b6459ed6c8862abb283f4cdee8ab4f03fd702f6ab747@ec2-52-206-38-187.compute-1.amazonaws.com:5432/d3pgbges6bt8l0'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jafjilbllqlkym:2917c8ddd24c8cace3eea776165605b1c45f4a4592a4779e7c17f19acabb4534@ec2-44-206-204-65.compute-1.amazonaws.com:5432/db8k0g41shj1bl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u7o2d5jvjh52jc:p14a765b8b1caa1850461e4103bc5b4c87562129c881295eefab20c020de72023@ec2-54-204-93-26.compute-1.amazonaws.com:5432/ddcu293t8mnpcm'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), unique=False)
    model = db.Column(db.String(100), unique=False)
    year = db.Column(db.String(100), unique=False)
    condition = db.Column(db.String(100), unique=False)
    mileage = db.Column(db.String(100), unique=False)
    photo = db.Column(db.String(1000), unique=False)
    description = db.Column(db.String(1000), unique=False)

    def __init__(self, make, model, year, condition, mileage, photo, description):
       self.make = make
       self.model = model
       self.year = year
       self.condition = condition 
       self.mileage = mileage 
       self.photo = photo 
       self.description = description 
       

class CarSchema(ma.Schema):
    class Meta:
        fields = ('id','make', 'model', 'year', 'condition', 'mileage', 'photo', 'description')

car_schema = CarSchema()
cars_schema = CarSchema(many=True)

#Endpoint to create a new car
@app.route('/car', methods=['POST'])
def add_Car():
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    condition = request.json['condition']
    mileage = request.json['mileage']
    photo = request.json['photo']
    description = request.json['description']

    new_car = Car(make, model, year, condition, mileage, photo, description)

    db.session.add(new_car)
    db.session.commit()

    car = Car.query.get(new_car.id)

    return car_schema.jsonify(car)

# Endpoint to query all blogs
@app.route('/cars', methods=['GET'])
def get_cars():
    all_cars = Car.query.all()
    result = cars_schema.dump(all_cars)
    return jsonify(result)

# Endpoint to query a single car
@app.route('/car/<id>', methods=["GET"])
def get_car(id):
    car = Car.query.get(id)
    return car_schema.jsonify(car)

# Endpoint for updating a car
@app.route("/car/<id>", methods=["PUT"])
def car_update(id):
    car = Car.query.get(id)
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    condition = request.json["condition"]
    mileage = request.json["mileage"]
    photo = request.json["photo"]
    description = request.json["description"]

    car.make = make
    car.model = model
    car.year = year
    car.condition = condition
    car.mileage = mileage
    car.photo = photo
    car.photo = description

    db.session.commit()
    return car_schema.jsonify(car)

# Endpoint for deleting a car
@app.route('/car/<id>', methods=['DELETE'])
def car_delete(id):
    car = db.session.query(Car).filter(Car.id == id).first()
    db.session.delete(car)
    db.session.commit()

    return car_schema.jsonify(car)

if __name__ == "__main__":
    app.run(debug=True)
