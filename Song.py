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
    '''
    This class is for playlist songs.
    Attribute:
        id (int): Song id, primary key.
        title (str): Title of song.
        artist (str): Artist of song.
        genre (str): Musical genre of song.
        youtube (str): Youtube video id.
        rendition (str):  If the song is a cover or a rendition of an older song.
        playlist_id (int): Id of the playlist to which song belongs, foreign key from playlist.
        playlist (obj): Object of of the playlist to which song belongs.
        user_id (int): User id of creator of playlist, foreign key from user.
        user (obj): User object of creator of playlist.
        time_created (datetime): Unix timestamp of when playlist was created.
        time_updated (datetime): Unix timestamp of when playlist was updated.
    '''
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
