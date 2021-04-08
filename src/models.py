from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    def __repr__(self):
        return '<User %r>' % self.username 
        # no es necesaria tenerla pero lo que esta funcion hace es permitir que se lea

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def uservalues():
        user_query = User.query.all()
        all_user = list(map(lambda x: x.serialize(), user_query))
        return all_user

    def add_user(request_body_user):
        user = User(fullname=request_body_user["fullname"], username=request_body_user["username"], email=request_body_user["email"], password=request_body_user["password"])
        db.session.add(user)
        db.session.commit()
        return("An user has been added")

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)
    skin_color = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def charactersvalues():
        characters_query = Character.query.all()
        all_characters = list(map(lambda x: x.serialize(), characters_query))
        return all_characters

    def add_character(request_body_character):
        character = Character(name=request_body_character["name"], birth_year=request_body_character["birth_year"], gender=request_body_character["gender"], height=request_body_character["height"], skin_color=request_body_character["skin_color"], eye_color=request_body_character["eye_color"])
        db.session.add(character)
        db.session.commit()
        return("A character has been added")


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(120), unique=True, nullable=False)
    orbital_period = db.Column(db.String(120), unique=False, nullable=False)
    rotation_period = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def planetsvalues():
        planets_query = Planet.query.all()
        all_planets = list(map(lambda x: x.serialize(), planets_query))
        return all_planets

    def add_planet(request_body_planet):
        planet = Planet(name=request_body_planet["name"], climate=request_body_planet["climate"], population=request_body_planet["population"], orbital_period=request_body_planet["orbital_period"], rotation_period=request_body_planet["rotation_period"], diameter=request_body_planet["diameter"])
        db.session.add(planet)
        db.session.commit()
        return("A planet has been added")