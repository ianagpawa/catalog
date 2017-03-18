from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Playlist, Song, User

engine = create_engine('sqlite:///musiccatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


session.query(User).filter_by(email="JC@test.com").first()
user1 = session.query(User).filter_by(email="BigTrouble@LittleChina.com").first()
user2 = session.query(User).filter_by(email="JC@test.com").first()
playlist = session.query(Playlist).filter_by(name="Test").first()
song2 = session.query(Song).filter_by(title="Test Title").first()
song1 = session.query(Song).filter_by(title="Another Test").first()
playlist2 = session.query(Playlist).filter_by(name="Blue").first()
song3 = session.query(Song).filter_by(title="Third Test Title").first()
song4 = session.query(Song).filter_by(title="The Boss").first()
playlist3 = session.query(Playlist).filter_by(name="Second Test").first()
song5 = session.query(Song).filter_by(title="Second test title").first()
song6 = session.query(Song).filter_by(title="Third Test").first()

session.delete(song1)
session.delete(song2)
session.delete(song3)
session.delete(song4)
session.delete(song5)
session.delete(song6)
session.delete(playlist)
session.delete(playlist2)
session.delete(playlist3)
session.delete(user1)
session.delete(user2)

session.commit()


#
# playlist = session.query(Playlist).filter_by(name="Test").first()
# playlist2 = session.query(Playlist).filter_by(name="thing").first()
# playlist3 = session.query(Playlist).filter_by(name="Blue").first()
# playlist4 = session.query(Playlist).filter_by(name="Second Test").first()
# session.delete(playlist)
# session.delete(playlist2)
# session.delete(playlist3)
# session.delete(playlist4)

#
