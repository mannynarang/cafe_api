import random

import first as first
from Tools.scripts.make_ctype import method
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for col in self.__table__.columns:
            dictionary[col.name] = getattr(self, col.name)

        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record


@app.route('/search', methods=['GET', 'POST'])
def search():
    fin = []
    if request.method == "GET":
        res = db.session.query(Cafe).filter_by(location=request.args.get('loc'))

        for r in res:
            fin.append(r.to_dict())

        if fin == []:
            return jsonify(error={"Not Found": "Sorry"})

    return jsonify(locations=fin)


@app.route("/random")
def rdandom():
    cafe = db.session.query(Cafe).all()
    cafe_list = random.choice(cafe)

    return jsonify(cafe=cafe_list.to_dict())


@app.route("/all")
def allz():
    all_cafe_list = []
    all_cafe = db.session.query(Cafe).all()
    for cafe in all_cafe:
        all_cafe_list.append(cafe.to_dict())

    return jsonify(cafes=all_cafe_list)


## HTTP POST - Create Record
@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        print(request.form['name'])
        print(request.form['map_url'])
        new_cafe = Cafe(name=request.form['name'],
                        map_url=request.form['map_url'],
                        img_url=request.form['img_url'],
                        location=request.form['location'],
                        seats=request.form['seats'],
                        has_toilet=bool(request.form['toilet']),
                        has_wifi=bool(request.form['wifi']),
                        has_sockets=bool(request.form['has_sockets']),
                        can_take_calls=bool(request.form['can_take_calls']),
                        coffee_price=request.form['coffee_price'])

    # new_cafe = Cafe(
    # name=request.form.get("name"),
    # map_url=request.form.get("map_url"),
    # img_url=request.form.get("img_url"),
    # location=request.form.get("loc"),
    # has_sockets=bool(request.form.get("sockets")),
    # has_toilet=bool(request.form.get("toilet")),
    # has_wifi=bool(request.form.get("wifi")),
    # can_take_calls=bool(request.form.get("calls")),
    # seats=request.form.get("seats"),
    # coffee_price=request.form.get("coffee_price"))

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record

@app.route("/update_price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    print("update_price")
    print(cafe_id)
    update = (db.session.query(Cafe).filter_by(id=cafe_id)).first()
    if update is None:
        return jsonify(response={"fail": "ID not found."})
    else:
        update.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully changed"})

    # new_price = request.args.get("new_price")
    # cafe = db.session.query(Cafe).get(cafe_id)
    # if cafe:
    #     cafe.coffee_price = new_price
    #     db.session.commit()


## HTTP DELETE - Delete Record
@app.route("/delete/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    key = request.args.get("api_key")
    if key is None:
        return jsonify(resource={"fail:": "no api key"}), 400

    else:
        delete = db.session.query(Cafe).filter_by(id=cafe_id).first()
        if delete is None:
            return jsonify(resource={"fail:": "no cafe found with that id"}), 400
        else:
            db.session.delete(delete)
            db.session.commit()
            return jsonify(resource={"Success": "Delete success"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=9004)
