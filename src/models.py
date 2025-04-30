from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_favorite_planets = Table(
    'user_favorite_planets',
    db.Model.metadata,
    db.Column('user_id', db.Integer, ForeignKey('user.id')),
    db.Column('planet_id', db.Integer, ForeignKey('planet.id'))
)

user_favorite_characters = Table(
    'user_favorite_characters',
    db.Model.metadata,
    db.Column('user_id', db.Integer, ForeignKey('user.id')),
    db.Column('character_id', db.Integer, ForeignKey('character.id'))
)

user_favorite_vehicles = Table(
    'user_favorite_vehicles',
    db.Model.metadata,
    db.Column('user_id', db.Integer, ForeignKey('user.id')),
    db.Column('vehicle_id', db.Integer, ForeignKey('vehicle.id'))
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    lastName: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planets = relationship("Planet", secondary=user_favorite_planets, backref="favorited_by_users")
    favorite_characters = relationship("Character", secondary=user_favorite_characters, backref="favorited_by_users")
    favorite_vehicles = relationship("Vehicle", secondary=user_favorite_vehicles, backref="favorited_by_users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nick": self.nick,
            "name": self.name,
            "lastName": self.lastName
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(200), nullable=False)
    gravity: Mapped[int] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "gravity": self.gravity
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet = relationship("Planet", backref="residents")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "planet_id": self.planet_id
        }

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    planet = relationship("Planet", backref="vehicles")
    character = relationship("Character", backref="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }
