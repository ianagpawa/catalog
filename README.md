# Aural History

##### This repo is for my item catalog project from the Udacity Full Stack Nanodegree course.    


### Quick Start
-Clone the repo: `git clone https://github.com/ianagpawa/catalog.git`

#### Setting up the database
Before viewing the app, while the terminal is in the project folder, use command `python db_setup.py` to create the database, `musiccatalog.db`.  Executing commands `python loadsongs.py` and `python loadfeatured.py` will populate the database with dummy data.

#### Viewing the app locally
In order to run the app locally, `vagrant` must be installed on your system, and your project folder must include the `Vagrantfile` and `pf_config.sh` files.

##### Install Virtualbox and Vagrant
`virtualbox` needs to be installed on your system before install `vagrant`.  To install `virtualbox` on Ubuntu:
1.  Edit file `/etc/apt/sources.list` by adding the line below (depends on your distribution - this one is for 16.04 Xenial) to the end of the file:
```
deb http://download.virtualbox.org/virtualbox/debian xenial contrib
```
2.  Download and import Oracle public key:
```
$ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
$ wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -

```
3.  Install Oracle Virtualbox with the following commands:
```
$ sudo apt-get update
$ sudo apt-get install virtualbox-5.1
```
4.  Install vagrant:
```
$ sudo apt install vagrant
```

With the terminal in the project folder, use command `vagrant up`, then command `vagrant ssh` to start the virtual desktop environment.  Then use the following commands to change to the project directory, and then run the app locally:
```
cd /vagrant
python main.py
```
Point your browser to `localhost:5000` to view the app.

### What's included
Within the project folder, you will find the following files:

```
catalog/
    ├── static/
    |    └── css/
    |         └── styles/
    |               └── main.css
    ├── templates/
    |    ├── base.html
    |    ├── deleteplaylist.html
    |    ├── deletesong.html
    |    ├── editplaylist.html
    |    ├── editsong.html
    |    ├── error.html
    |    ├── featuredsingle.html
    |    ├── loggedin.html
    |    ├── login.html
    |    ├── newfeatured.html
    |    ├── newplaylist.html
    |    ├── newsong.html    
    |    ├── playlists.html
    |    ├── publicplaylists.html
    |    ├── publicsongs.html
    |    ├── single.html    
    |    └── songs.html
    ├── app.yaml
    ├── Base.py
    ├── client_secrets.json
    ├── db_setup.py
    ├── deletesongs.py    
    ├── fb_client_secrets.json
    ├── Featured.py   
    ├── loadfeatured.py  
    ├── main.py    
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

 agpawaji@gmail.com
