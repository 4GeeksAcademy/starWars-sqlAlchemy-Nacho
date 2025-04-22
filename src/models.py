from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(200),nullable=False)
    name: Mapped[str] = mapped_column(String(200),nullable=False)
    lastName: Mapped[str] = mapped_column(String(200),nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nick":self.nick,
            "name":self.name,
            "lastName":self.lastName
            # do not serialize the password, its a security breach
        }
class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    

    def serialize(self):
        return {
            "planet": self.planet_id,
            "character": self.character_id,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_id: Mapped[int]= mapped_column(ForeignKey("favorite.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"))
    name: Mapped[str] = mapped_column(String(200),nullable=False)
    poblation: Mapped[int] = mapped_column(nullable=False)
    climated: Mapped[str] = mapped_column(String(200),nullable=False)
    gravity: Mapped[int] = mapped_column(nullable=False)


    def serialize(self):
        return {
            "name": self.name,
            "poblation": self.poblation,
            "climated":self.climated,
            "gravity":self.gravity
        }
class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_id: Mapped[int]= mapped_column(ForeignKey("favorite.id"))
    planet_id: Mapped[int] =mapped_column(ForeignKey("planet.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"))
    name: Mapped[str] = mapped_column(String(200),nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "name": self.name,
            "planet": self.planet_id,
            "vehicle": self.vehicle_id,
            "name":self.name,
            "mass":self.mass

        }
class vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorite.id"))
    character_id:Mapped[int] = mapped_column(ForeignKey("character.id"))
    planet_id: Mapped[int] =mapped_column(ForeignKey("planet.id"))
    name: Mapped[str] = mapped_column(String(200),nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    def serialize(self):
        return {
            "character": self.character_id,
            "name":self.name,
            "mass":self.mass,
            "planet": self.planet_id,
        }