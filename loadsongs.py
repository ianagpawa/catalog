
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


# Create dummy user
User1 = User(name="Jack Burton", email="BigTrouble@LittleChina.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Jacque Chen", email="JC@test.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

User3 = User(name="Jacque Chen", email="JC@test.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User3)
session.commit()


# Songsfor playlist1
playlist1 = Playlist(user_id=1, name="Test", description='First test playlist')

session.add(playlist1)
session.commit()



song2 = Song(user_id=1,
                title="Test Title",
                artist='Test Artist',
                genre="Test",
                youtube="8Oh18uHnrn4",
                playlist=playlist1)

session.add(song2)
session.commit()


song1 = Song(user_id=1,
                title="Another Test",
                artist='Another Artist',
                genre="Funk",
        		youtube="jC2ZY2loo74",
        		rendition='Tighten Up',
                playlist=playlist1)

session.add(song1)
session.commit()

# Playlist for playlist2
playlist2 = Playlist(user_id=2, name="Blue", description="It's Blue")

session.add(playlist2)
session.commit()

song3 = Song(user_id=2,
                title="Third Test Title",
                artist="Third Test Artist",
                genre="rock",
                playlist=playlist2)

session.add(song3)
session.commit()


song4 = Song(user_id=2,
                title="The Boss",
                artist='James Brown',
                genre="Funk",
                youtube="jC2ZY2loo74",
                playlist=playlist2)

session.add(song4)
session.commit()


print "added playlist songs!"
