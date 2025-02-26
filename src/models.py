from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos = db.relationship("Favoritos",backref="user",lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    size = db.Column(db.String(80))
    color = db.Column(db.String(80))
    temp =  db.Column(db.Integer)
    favoritos = db.relationship("Favoritos", backref="planet", lazy=True)

    # def __repr__(self):
    #     return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "name" : self.name,
            "id": self.id,
            "size": self.size,
            "color" : self.color,
            "temp" : self.temp
            
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    faccion = db.Column(db.String(80))
    job = db.Column(db.String(80))
    race =  db.Column(db.String(80))
    favoritos = db.relationship("Favoritos", backref="people", lazy=True)

    def serialize(self):
        return {
            "name" : self.name,
            "id": self.id,
            "faccion": self.faccion,
            "job" : self.job,
            "race" : self.race
            # do not serialize the password, its a security breach
        }
    

class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id =db.Column(db.Integer, db.ForeignKey("planet.id"))
    people_id= db.Column(db.Integer, db.ForeignKey("people.id"))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people": self.people.serialize() if self.people else None,
            "planet": self.planet.serialize() if self.planet else None
            # do not serialize the password, its a security breach
        }


