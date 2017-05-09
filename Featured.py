import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from Base import Base
from User import User

class Featured(Base):
    '''
    This class is for songs in the special playlist, Featured.
    Attribute:
        id (int): Song id, primary key.
        title (str): Title of song.
        artist (str): Artist of song.
        genre (str): Musical genre of song.
        youtube (str): Youtube video id.
        rendition (str):  If the song is a cover or a rendition of an older song.
        user_id (int): User id of creator of playlist, foreign key from user.
        user (obj): User object of creator of playlist.
        time_created (datetime): Unix timestamp of when playlist was created.
        time_updated (datetime): Unix timestamp of when playlist was updated.
    '''
    __tablename__ = 'featured'
    id = Column(Integer, primary_key = True)
    title = Column(String(80), nullable = False)
    artist = Column(String(80), nullable = False)
    genre = Column(String(80))
    youtube = Column(String(250))
    rendition = Column(String(80))
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
            'time_created': self.time_created.strftime("%B %d, %Y")
        }
