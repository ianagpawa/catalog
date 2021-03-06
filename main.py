from flask import Flask, render_template, request, redirect, url_for, flash, \
                    make_response, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Playlist, Song, Featured
#   imports for authentication
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from functools import wraps
import pprint

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Music Catalog Application'

app = Flask(__name__)

engine = create_engine('sqlite:///musiccatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_playlist(playlist_id):
    '''
    get_playlist: Method for getting playlist for catalog.
    Args:
        playlist_id (int): Playlist ID number.
    Returns:
        Object of the playlist
    '''
    return session.query(Playlist).filter_by(id=playlist_id).one()


def add_to_db(obj):
    '''
    add_to_db: Method for adding objects to database.
    Args:
        obj (obj): Database object (user, song, or playlist)
    '''
    session.add(obj)
    session.commit()

@app.context_processor
def my_utility_process():
    def get_latest_song(playlist_id):
        return session.query(Song).filter_by(playlist_id=playlist_id).order_by(desc(Song.id))[0]

    def get_number_of_songs(playlist_id):
        return session.query(Song).filter_by(playlist_id=playlist_id).count()

    return dict(get_latest_song=get_latest_song, get_number_of_songs=get_number_of_songs)

def login_required(func):
    '''
    login_required: function decorator for checking if user is logged in

    Returns:
        If not logged in, redirects to login page.
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' in login_session:
            return func(*args, **kwargs)
        else:
            flash("You are not allowed to acces this without logging in!")
            return redirect("/login")
    return decorated_function


@app.route("/playlists/JSON/")
def showPlaylistsJSON():
    '''
    showPlaylistsJSON: Method for JSON output of playlists route
    '''
    playlists = session.query(Playlist).all()
    return jsonify(Playlists=[playlist.serialize for playlist in playlists])


@app.route("/")
@app.route("/playlists/")
def showPlaylists():
    '''
    showPlaylists:  Method for home ('/') or playlists route.

    Returns:
        Playlists page for home or playlists route.  If a user is not signed
        in a playlists page with no 'edit' or 'delete' buttons will be
        returned.
    '''
    songs = session.query(Song).order_by(Song.id.desc())
    songList = getSongList(songs)
    playlists = session.query(Playlist).order_by(Playlist.id)
    featured = session.query(Featured).order_by(Featured.id.desc()).first()
    if 'username' not in login_session:
        return render_template('publicplaylists.html', playlists=playlists,
                                songList=songList, featured=featured)
    else:
        return render_template("playlists.html", playlists=playlists,
                                songList=songList, featured=featured)





#TODO Change to match featured.  need to have regulr /featured
@app.route("/featured/new/",
           methods=['GET', 'POST'])
def newSongFeatured():
    '''
    newSong: Method adding a new featured song.

    Returns:
        If not logged in, redirects to login page.  Only Creator can add to
        this playlist.  Displays errors when song title or arist is not
        included.  Redirects to home page after adding the song.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['email'] != 'agpawaji@gmail.com':
        return redirect(url_for('showPlaylists'))


    if request.method == "POST":
        if request.form['featured-title'] and request.form['featured-artist']:
            title = request.form['featured-title']
            artist = request.form['featured-artist']
            genre = request.form['featured-genre']
            youtube = None
            if request.form['featured-youtube']:
                link = request.form['featured-youtube']
                if '//youtu.be' in link:
                    checkQ = link.split("/")[3]
                else:
                    checkQ = link.split('=')[1]
                vid_id = checkQ.split("&")[0]
                youtube = vid_id
            rendition = request.form['featured-rendition']
            newFeatured = Featured(title=title,
                           artist=artist,
                           genre=genre,
                           youtube=youtube,
                           rendition=rendition)
            add_to_db(newFeatured)
            flash('A new song was added to the Featured playlist')
            return redirect(url_for('showPlaylists'))
        else:
            flash("Song title and Artist is required!")
            return render_template('newfeatured.html')
    else:
        return render_template('newfeatured.html')


@app.route("/playlists/new/", methods=['GET', 'POST'])
@login_required
def newPlaylist():
    '''
    newPlaylist:    Method for new playlists page.

    Returns:
        Renders page for adding new playlists.  To add new playlist, a playlist
        name is required.  If user is not logged in,redirects to login page.
        Once added, redirects to home.

    '''
    if request.method == 'POST':
        playlist_name = request.form['playlist_name']
        if playlist_name:
            playlist_description = request.form['playlist_description']
            user_id = login_session['user_id']
            newPlaylist = Playlist(name=playlist_name,
                                   description=playlist_description,
                                   user_id=user_id)
            add_to_db(newPlaylist)
            flash("New playlist (%s) was created!" % playlist_name)
            return redirect(url_for('showPlaylists'))
        else:
            flash("A playlist name is required!")
            return render_template("newplaylist.html")
    else:
        return render_template("newplaylist.html")


@app.route("/playlist/<int:playlist_id>/edit/", methods=['GET', 'POST'])
@login_required
def editPlaylist(playlist_id):
    '''
    editPlaylist:   Method for editing playlists.
    Args:
        playlist_id (int): Playlist id number.
    Returns:
        If not logged in, redirects to login page.  If user is not creator of
        playlist, redirected to an error page.  Playlist name and description
        can be editted, and must include at least playlist name to proceed.
        Once editted, redirects to home page.
    '''

    playlist = get_playlist(playlist_id)

    if playlist.user_id != login_session['user_id']:
        error = '''
        You are not authorized to edit this playlist.
        Please create your own playlist in order to edit.
        '''
        return render_template("error.html", error=error)

    if request.method == 'POST':
        if request.form['edit_playlist_name']:
            editted_name = request.form['edit_playlist_name']
            playlist.name = editted_name
        else:
            flash("Playlist name is needed!")
            return render_template("editplaylist.html", playlist=playlist)
        editted_description = request.form['edit_playlist_description']
        playlist.description = editted_description

        add_to_db(playlist)
        flash('Playlist name has been edited!')
        return redirect(url_for('showPlaylists'))
    else:
        return render_template("editplaylist.html", playlist=playlist)


@app.route("/playlist/<int:playlist_id>/delete/",
           methods=['GET', 'POST'])
@login_required
def deletePlaylist(playlist_id):
    '''
    deletePlaylist: Method for deleting playlists.

    Args:
        playlist_id (int): Playlist ID number.

    Returns:
        If user not login, redirects to login page.  If user is not creator of
        the playlist, redirects to error page.  After deletion redirects to
        home page.

    '''

    playlist = session.query(Playlist).filter_by(id=playlist_id).one()

    if playlist.user_id != login_session['user_id']:
        error = '''
        You are not authorized to delete this playlist.
        Please create your own playlist in order to delete.
        '''
        return render_template('error.html', error=error)

    if request.method == 'POST':
        if request.form['delete_playlist']:
            session.delete(playlist)
            session.commit()
            flash('Playlist has been deleted!')
            return redirect(url_for('showPlaylists'))
    else:
        return render_template('deleteplaylist.html', playlist=playlist)


def getSongs(playlist_id):
    '''
    getSongs:   Method for retrieving songs in a playlist.

    Args:
        playlist_id (int):  Playlist ID number.

    Returns:
        Array of songs.
    '''
    return session.query(Song).filter_by(playlist_id=playlist_id).order_by(desc(Song.id))


def getSongList(songs):
    songList = ""
    for song in songs:
        url = song.youtube
        if song != songs[-1]:
            songList += url + ","
        else:
            songList += url
    return songList


@app.route("/playlist/<int:playlist_id>/songs/JSON")
def showSongsJSON(playlist_id):
    '''
    showSongsJSON:  Method for JSON of songs in a playlist.

    Args:
        playlist_id (int):  Playlist ID number

    Returns:
        JSON of songs metadata in a playlist.
    '''
    playlist = get_playlist(playlist_id)
    songs = getSongs(playlist_id)
    return jsonify(Songs=[song.serialize for song in songs])


@app.route("/playlist/<int:playlist_id>/")
@app.route("/playlist/<int:playlist_id>/songs/")
def showSongs(playlist_id):
    '''
    showSongs:  Method for page dispalying list of songs in a playlist.

    Args:
        playlist_id (int):  Playlist ID number.

    Returns:
        If user logged in, renders songs.html with CRUD buttons.  Otherwise,
        renders page without CRUD buttons.

    '''
    playlist = get_playlist(playlist_id)
    songs = getSongs(playlist_id)
    songList = getSongList(songs)
    creator = getUserInfo(playlist.user_id)
    if (('username' not in login_session) or
       (creator.id != login_session['user_id'])):
        return render_template('publicsongs.html',
                               songs=songs,
                               songList=songList,
                               playlist=playlist,
                               creator=creator)
    else:
        return render_template('songs.html',
                               playlist=playlist,
                               songs=songs,
                               songList=songList,
                               creator=creator)


@app.route('/playlist/<int:playlist_id>/songs/<int:song_id>/JSON/')
def showSingleJSON(playlist_id, song_id):
    '''
    showSingleJSON: Method for JSON of a song.

    Args:
        playlist_id (int):  Playlist ID number.
        song_id (int):  Song ID number.

    Returns:
        JSON of song object.
    '''
    song = session.query(Song).filter_by(id=song_id).one()
    return jsonify(Song=song.serialize)


def spacing(name):
    return "%20".join(name.split(' '))

def appended(string):
  end = string.find('<a')
  return string[:end]

def api_method(method, api_key, artist, title):
    return "http://ws.audioscrobbler.com/2.0/?method=%s&api_key=%s&artist=%s&track=%s&format=json" % (method, api_key, spacing(artist), spacing(title))


@app.route('/playlist/<int:playlist_id>/songs/<int:song_id>/')
def showSingle(playlist_id, song_id):
    '''
    showSingle: Method for single song page.

    Args:
        playlist_id (int):  Playlist ID number.
        song_id (int):  Song ID number.

    Returns:
        Page for a single song.
    '''
    song = session.query(Song).filter_by(id=song_id).one()
    api_key = json.loads(open('last.json', 'r').read())[
        'web']['api_key']
    # api_url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=%s&artist=%s&track=%s&format=json" % (api_key, spacing(song.artist), spacing(song.title))

    api_url = api_method('track.getInfo', api_key, song.artist, song.title)

    try:
        h = httplib2.Http()
        song_info = json.loads(h.request(api_url, "GET")[1])['track']
        try:
            album = song_info['album']['title']
        except:
            album = ""
        try:
            album_link = song_info['album']['url']
        except:
            album_link = ""
        try:
            tags = song_info['toptags']['tag']
        except:
            tags = []
        try:
            song_url = song_info['url']
        except:
            song_url = ''
        try:
            wiki = song_info['wiki']
            try:
                wiki_content = wiki['content']
            except:
                wiki_content = ''
            try:
                wiki_summary = appended(wiki['summary'])
            except:
                wiki_summary = ''
        except:
            wiki = ''
            wiki_content = ''
            wiki_summary = ''
        retrieved_info = {
            'album': album,
            'album_link': album_link,
            'tags': tags,
            'song_url': song_url,
            'wiki_content': wiki_content,
            'wiki_summary': wiki_summary
        }
    except:
        retrieved_info = {}


    return render_template('single.html', song=song, retrieved_info=retrieved_info)


@app.route('/featured/<int:featured_song_id>/')
def showFeaturedSingle(featured_song_id):
    '''
    showSingle: Method for single Featured song page.

    Args:
        featured_song_id (int):  Featured song ID number.

    Returns:
        Page for a single song.
    '''
    featured = session.query(Featured).filter_by(id=featured_song_id).one()
    return render_template('featuredsingle.html', featured=featured)

@app.route("/playlist/<int:playlist_id>/songs/new/",
           methods=['GET', 'POST'])
def newSong(playlist_id):
    '''
    newSong: Method adding a song to a playlist.

    Args:
        playlist_id (int):  Playlist ID number.

    Returns:
        If not logged in, redirects to login page.  Displays errors when song
        title or arist is not included.  Redirects to playlist page after
        adding the song.
    '''
    if 'username' not in login_session:
        return redirect('/login')
    playlist = get_playlist(playlist_id)
    if request.method == "POST":
        if request.form['title'] and request.form['artist']:
            title = request.form['title']
            artist = request.form['artist']
            genre = request.form['genre']
            youtube = None
            if request.form['youtube']:
                link = request.form['youtube']
                if '//youtu.be' in link:
                    checkQ = link.split("/")[3]
                else:
                    checkQ = link.split('=')[1]
                vid_id = checkQ.split("&")[0]
                youtube = vid_id
            rendition = request.form['rendition']
            newSong = Song(title=title,
                           artist=artist,
                           genre=genre,
                           youtube=youtube,
                           rendition=rendition,
                           playlist_id=playlist_id,
                           user_id=playlist.user_id)
            add_to_db(newSong)
            flash('A new song was added to %s' % playlist.name)
            return redirect(url_for('showSongs', playlist_id=playlist_id))
        else:
            flash("Song title and Artist is required!")
            return render_template('newsong.html', playlist=playlist)
    else:
        return render_template('newsong.html', playlist=playlist)


@app.route("/playlist/<int:playlist_id>/songs/<int:song_id>/edit/",
           methods=['GET', 'POST'])
@login_required
def editSong(playlist_id, song_id):
    '''
    editSong: Method for uptdating song info.

    Args:
        playlist_id (int):  Playlist ID number.
        song_id (int):  Song ID number.

    Returns:
        If not logged in, redirects to login page.  If user is not the creator
        of the song, redirects to error page.  Errors are flashed if song
        title or artist fields are not filled.  Redirects to playlist page
        after editting.
    '''

    playlist = get_playlist(playlist_id)
    song = session.query(Song).filter_by(id=song_id).one()

    if login_session['user_id'] != playlist.user_id:
        error = '''
            You are not authorized to edit songs for this playlist.
            Please create your own playlist in order to edit songs.
        '''
        return render_template('error.html', error=error)

    if request.method == "POST":
        if not ((request.form['edit_title']) and
           (request.form['edit_artist'])):
            flash('Both title and artist is required!')
            return render_template('editsong.html', playlist=playlist,
                                   song=song)
        else:
            if request.form['edit_title']:
                editted_title = request.form['edit_title']
                song.title = editted_title
            if request.form['edit_artist']:
                editted_artist = request.form['edit_artist']
                song.artist = editted_artist
            if request.form['edit_genre']:
                editted_genre = request.form['edit_genre']
                song.genre = editted_genre
            if request.form['edit_youtube']:
                link = request.form['edit_youtube']
                if '//youtu.be' in link:
                    checkQ = link.split("/")[3]
                else:
                    checkQ = link.split('=')[1]
                vid_id = checkQ.split("&")[0]
                editted_youtube = vid_id
                song.youtube = editted_youtube
            if request.form['edit_rendition']:
                editted_rendition = request.form['edit_rendition']
                song.rendition = editted_rendition
            add_to_db(song)
            flash("(%s) was edited!" % song.title)
            return redirect(url_for('showSongs', playlist_id=playlist_id))
    else:
        return render_template('editsong.html', playlist=playlist,
                               song=song)


@app.route("/playlist/<int:playlist_id>/songs/<int:song_id>/delete/",
           methods=['GET', 'POST'])
@login_required
def deleteSong(playlist_id, song_id):
    '''
    deleteSong: Method deleting a song from a playlist.

    Args:
        playlist_id (int):  Playlist ID number.
        song_id (int):  Song ID number.

    Returns:
        If not logged in, redirects to login.  If user is not creator
        of playlist, redirects to error page.  Redirects to playlist
        after deletion.
    '''

    playlist = get_playlist(playlist_id)
    song = session.query(Song).filter_by(id=song_id).one()

    if login_session['user_id'] != playlist.user_id:
        error = '''
            You are not authorized to delete songs for this playlist.
            Please create your own playlist in order to delete songs.
        '''
        return render_template("error.html", error=error)

    if request.method == 'POST':
        if request.form['delete_song']:
            session.delete(song)
            session.commit()
            flash('A song was deleted!')
            return redirect(url_for('showSongs', playlist_id=playlist_id))
    else:
        return render_template('deletesong.html', song=song)


def createUser(login_session):
    '''
    createUser: Method for adding user to database.

    Args:
        login_session (obj):    User metadata retrieved from Google or
                                Facebook profiles.

    Returns:
        User ID number.
    '''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    '''
    getUserInfo: Method for retrieving user by their ID number

    Args:
        user_id (int):   User ID number

    Returns:
        User object.
    '''
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''
    getUserID:  Method for retrieving user by their email address.

    Args:
        email (str):    User email address.

    Returns:
        User object with corresponding email address.  Otherwise, None.
    '''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    '''
    showLogin: Method for logging into site using Google or
                Facebook authentication.

    Returns:
        Renders login page.
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    gconnect: Method for logging into site using Google authentication.

    Returns:
        Renders logged in page, then redirects to home page.
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 "Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    print "done!"
    # print login_session
    return render_template("loggedin.html", login_session=login_session)

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    '''
    gdisconnect: Method for logging out of site, revokes user's Google tokens.

    Returns:
        Redirects to home page.
    '''
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    '''
    fbconnect:  Method for logging into site via Facebook authentication.

    Returns:
        Renders login page, then redirects to home page.
    '''

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    # strip expire tag from access token
    token = result.split(',')[0].split(':')[1].replace('"', '')



    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    # sys.stdout = open('output.logs', 'w')
    # print (data["name"]) # Nothing appears below
    # print (data["email"]) # Nothing appears below
    # print (data["id"]) # Nothing appears below
    # sys.stdout = sys.__stdout__ # Reset to the standard output
    # open('output.logs', 'r').read()
    # return "OK"
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Now logged in as %s" % login_session['username'])
    return render_template("loggedin.html", login_session=login_session)


@app.route('/fbdisconnect')
def fbdisconnect():
    '''
    fbdisconnect:   Method for logging out of site by revoking user's
                    Facebook tokens.

    Returns:
        Redirects to home page after notifcation.
    '''
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ("https://graph.facebook.com/%s/permissions"
           "?access_token=%s") % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    '''
    disconnect: Method for logging out of site

    Returns:
        Redirects to home page.
    '''
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
# NOT SURE IF NEEDED, disconnect does not work otherwise
#            del login_session['credentials']
            del login_session['gplus_id']

        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        del login_session['access_token']
        del login_session['state']
        flash("You have successfully been logged out.")
        return redirect(url_for('showPlaylists'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showPlaylists'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
