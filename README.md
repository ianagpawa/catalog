# Aural History
### By Ian Agpawa
##### This repo is for my item catalog project from the Udacity Full Stack Nanodegree course.    


### Quick Start
-Clone the repo: `git clone https://github.com/ianagpawa/catalog.git`

#### Setting up the database
Before viewing the app, while the terminal is in the project folder, use command `python db_setup.py` to create the database, `musiccatalog.db`.  Executing `python loadsongs.py` will populate the database with dummy data.

#### Viewing the app locally
In order to run the app locally, `vagrant` must be installed on your system, and your project folder must include the `Vagrantfile` and `pf_config.sh` files.

With the terminal in the project folder, use command `vagrant up`, then command `vagrant ssh`.  When in the virtual desktop environment, use command `cd /vagrant` to change to the project directory and execute `python catalog.py` to run the app locally.  Point your browser to `localhost:5000` to view the app.

### What's included
Within the project folder, you will find the following files:

```
catalog/
    ├── static/
    |    ├── css/
    |    |    └── styles/
    |    |          └── main.css
    ├── templates/
    |    ├── base.html
    |    ├── deleteplaylist.html
    |    ├── deletesong.html
    |    ├── editplaylist.html
    |    ├── editsong.html
    |    ├── error.html
    |    ├── loggedin.html
    |    ├── login.html
    |    ├── newplaylist.html
    |    ├── newsong.html    
    |    ├── playlists.html
    |    ├── publicplaylists.html
    |    ├── publicsongs.html
    |    ├── single.html    
    |    └── songs.html
    ├── Base.py
    ├── catalog.py
    ├── client_secrets.json
    ├── db_setup.py
    ├── fb_client_secrets.json
    ├── loadsongs.py
    ├── pg_config.sh
    ├── Playlist.py
    ├── README.md
    ├── Song.py
    ├── User.py
    └── Vagrantfile
```

## Creator

**Ian Agpawa**


[Github](https://github.com/ianagpawa)

 agpawaji@gmail.com
