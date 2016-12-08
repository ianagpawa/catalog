import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from bson import json_util
import json

from Base import Base

class User(Base):
    '''
    This class is for users of the catalog, inherits from Base.
    Attribute:
        id (int): User id, primary key.
        name (str): Name of user.
        email (str): Email of user.
        pciture (str): Link for user profile picture.
        time_created (datetime): Unix timestamp of when playlist was created.
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(320), nullable = False)
    picture = Column(String(250))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'time_created': self.time_created.strftime("%B %d, %Y")
        }
