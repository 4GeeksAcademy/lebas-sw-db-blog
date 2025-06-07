from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, DateTime, Enum as SqlEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
    favorites: Mapped[list["Favorites"]] = relationship("Favorites", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            # do not serialize the password, it's a security breach
        }

class Category(Enum):
    Character = "character"
    Planet = "planet"
    Vehicle = "vehicle"            

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    post_title: Mapped[str] = mapped_column(String(255), nullable=False)
    post_text: Mapped[str] = mapped_column(String(2200), nullable=False)
    tag_cat: Mapped[Category] = mapped_column(SqlEnum(Category, name="category_enum"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    author: Mapped["User"] = relationship("User", back_populates="posts")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="post")

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    OTHER = "other"

class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_type: Mapped[MediaType] = mapped_column(SqlEnum(MediaType, name="media_type_enum"), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('POST.id'), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "media_type": self.media_type.value,
            "url": self.url
        }

class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(1000), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('POST.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now())
    
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fav_user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('POST.id'), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="favorites")

class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    homeworld: Mapped[str] = mapped_column(String(100))
    species: Mapped[str] = mapped_column(String(100))
    
    favorites: Mapped[list["CharacterFavorite"]] = relationship("CharacterFavorite", back_populates="character")

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    population: Mapped[int]
    
    favorites: Mapped[list["PlanetFavorite"]] = relationship("PlanetFavorite", back_populates="planet")

class CharacterFavorite(db.Model):
    __tablename__ = 'character_favorite'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=False)

    user: Mapped["User"] = relationship("User", backref="character_favorites")
    character: Mapped["Character"] = relationship("Character", back_populates="favorites")

class PlanetFavorite(db.Model):
    __tablename__ = 'planet_favorite'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=False)

    user: Mapped["User"] = relationship("User", backref="planet_favorites")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorites")
