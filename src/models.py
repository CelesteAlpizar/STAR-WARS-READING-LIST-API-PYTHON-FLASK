from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
favorite_characters = db.Table('favorite_characters', db.Column('user_id', db.Integer, db.ForeignKey('usuario.id')), db.Column('character_id', db.Integer, db.ForeignKey('personaje.id')))
favorite_planets = db.Table('favorite_planets', db.Column('user_id', db.Integer, db.ForeignKey('usuario.id')), db.Column('planet_id', db.Integer, db.ForeignKey('planeta.id')))


class User(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    personaje = db.relationship('Character', secondary=favorite_characters, back_populates="usuario")
    planeta = db.relationship('Planet', secondary=favorite_planets, back_populates="usuario")

    def __repr__(self):
        return '<User %r>' % self.username 
        # no es necesaria tenerla pero lo que esta funcion hace es permitir que se lea

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            "characters": list(map(lambda x: x.serialize(), self.personaje)),
            "planets": list(map(lambda x: x.serialize(), self.planeta))
            # do not serialize the password, its a security breach
        }

    def getAll_users():
        user_query = User.query.all()
        all_user = list(map(lambda x: x.serialize(), user_query))
        return all_user

    def getOne_user(id):
        user_query = User.query.get(id)
        return(user_query.serialize())

    def add_user(request_body_user):
        user = User(fullname=request_body_user["fullname"], username=request_body_user["username"], email=request_body_user["email"], password=request_body_user["password"])
        db.session.add(user)
        db.session.commit()
        return("The user has been created")

    def remove_User(id):
        user = User.query.get(id)
        if user is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user)
        db.session.commit()
        return("The user has been deleted")


    def user_fav_characters(id, character_id):
        user = User.query.get(id)
        character_id = Character.query.get(character_id) 
        if user is None:
            raise APIException('User not found', status_code=404)
        if char is None:
            raise APIException('Character not found', status_code=404)

        user.characters.append(char)
        db.session.commit()
        return user.serialize()

    def user_fav_planets(id, planet_id):
        user = User.query.get(id)
        planet = Planet.query.get(planet_id) 
        if user is None:
            raise APIException('User not found', status_code=404)
        if planet is None:
            raise APIException('Planet not found', status_code=404)
       
        user.planets.append(planet)
        db.session.commit()
        return user.serialize()


class Character(db.Model):
    __tablename__ = 'personaje'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)
    skin_color = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=False)

    usuario = db.relationship("User", secondary=favorite_characters, back_populates="personaje")

    def __repr__(self):
        return '<Character %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def getAll_characters():
        characters_query = Character.query.all()
        all_characters = list(map(lambda x: x.serialize(), characters_query))
        return all_characters

# No se si esta es necesaria puesto que los usuarios tendrian acceso a toda la informacion del personaje sin esto 
    def getOne_character(id):
        character_query = Character.query.get(id)
        return(char_query.serialize())

# No se si esta necesaria puesto que los caracteres ya estarian agregados
    def add_character(request_body_character):
        character = Character(name=request_body_character["name"], birth_year=request_body_character["birth_year"], gender=request_body_character["gender"], height=request_body_character["height"], skin_color=request_body_character["skin_color"], eye_color=request_body_character["eye_color"])
        db.session.add(character)
        db.session.commit()
        return("A character has been added")


class Planet(db.Model):
    __tablename__ = 'planeta'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(120), unique=True, nullable=False)
    orbital_period = db.Column(db.String(120), unique=False, nullable=False)
    rotation_period = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.String(120), unique=False, nullable=False)

    usuario = db.relationship("User", secondary=favorite_planets, back_populates="planeta") 

    def __repr__(self):
        return '<Planet %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def getAll_planets():
        planets_query = Planet.query.all()
        all_planets = list(map(lambda x: x.serialize(), planets_query))
        return all_planets

    # No se si esta es necesaria puesto que los usuarios tendrian acceso a toda la informacion del personaje sin esto 
    def getOne_planet(id):
        planet_query = Planet.query.get(id)
        return(char_query.serialize())

    def add_planet(request_body_planet):
        planet = Planet(name=request_body_planet["name"], climate=request_body_planet["climate"], population=request_body_planet["population"], orbital_period=request_body_planet["orbital_period"], rotation_period=request_body_planet["rotation_period"], diameter=request_body_planet["diameter"])
        db.session.add(planet)
        db.session.commit()
        return("A planet has been added")