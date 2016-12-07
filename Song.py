import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from bson import json_util
import json

from Base import Base
from User import User
from Playlist import Playlist

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
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'youtube': "https://www.youtube.com/watch?v=%s" % self.youtube,
            'rendition': self.rendition,
            'playlist_id': self.playlist_id,
            'user_id': self.user_id,
            'time_created': json.dumps(self.time_created, default=json_util.default),
            'time_updated': json.dumps(self.time_updated, default=json_util.default)
        }
