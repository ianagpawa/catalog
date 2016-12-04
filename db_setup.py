import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(320), nullable = False)
    picture = Column(String(250))
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'user': self.user
        }


##      add date created
class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key = True)
    title = Column(String(80), nullable = False)
    artist = Column(String(80), nullable = False)
    genre = Column(String(80))
    youtube = Column(String(250))
    rendition = Column(String(80))
    playlist_id = Column(Integer, ForeignKey('playlist.id'))
    playlist = relationship(Playlist)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'youtube': self.youtube,
            'rendition': self.rendition,
            'playlist_id': self.playlist_id,
            'playlist': self.playlist,
            'user_id': self.user_id,
            'user': self.user
        }


engine = create_engine('sqlite:///musiccatalog.db')

Base.metadata.create_all(engine)
