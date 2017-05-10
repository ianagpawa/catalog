import os
import sys
from sqlalchemy import create_engine

from User import User
from Playlist import Playlist
from Song import Song
from Featured import Featured

from Base import Base

engine = create_engine('sqlite:///musiccatalog.db')

Base.metadata.create_all(engine)
