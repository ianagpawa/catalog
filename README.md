# Aural History
### By Ian Agpawa
##### This repo is for my item catalog project from the Udacity Full Stack Nanodegree course.    


### Quick Start
-Clone the repo: `git clone https://github.com/ianagpawa/catalog.git`

#### Setting up the database
Before viewing the app, the database must be set up.  While in the project folder, use command `python db_setup.py`.  The `lotsofsongs.py` file is included to populate the database, which can be done by executing `python lotsofsongs.py` after setting up the database.
#### Viewing the app locally
In order to run the app locally, `vagrant` must be installed on your system, and your project folder must include the `Vagrantfile` and `pf_config.sh` files.  With the terminal in the project folder location, use command `vagrant up`, then when use `vagrant ssh`.  When in the virtual desktop environment, use command `cd /vagrant` to change to the project directory and then, you can use command `python catalog.py` to run the app locally.  Point your browser to `localhost:5000` to view the app.
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
    |    ├── login.html
    |    ├── newplaylist.html
    |    ├── newsong.html    
    |    ├── playlists.html
    |    ├── publicplaylists.html
    |    ├── publicsongs.html
    |    ├── single.html    
    |    └── songs.html
    ├── app.yaml
    ├── Comment.py
    ├── Handler.py
    ├── index.yaml
    ├── Login.py
    ├── Logout.py
    ├── main.py
    ├── NewPostPage.py
    ├── Post.py
    ├── PostPage.py
    ├── README.md
    ├── SignUpPage.py
    ├── User.py
    └── WelcomePage.py
```

## Creator

**Ian Agpawa**


[Github](https://github.com/TheArtilect)

 agpawaji@gmail.com
