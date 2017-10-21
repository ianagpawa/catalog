# Aural History

##### This repo is for my item catalog project from the Udacity Full Stack Nanodegree course.    


## Quick Start
-Clone the repo: `git clone https://github.com/ianagpawa/catalog.git`

### Setting up the database
Before viewing the app, while the terminal is in the project folder, use command `python db_setup.py` to create the database, `musiccatalog.db`.  Executing commands `python loadsongs.py` and `python loadfeatured.py` will populate the database with dummy data.

### Requirements
This app requires API keys from Facebook, Google, and Last.fm, and you will need to register and get API keys from each.  Each API key should be saved as a `JSON` file and located in the root level of the project.

#### Facebook
`fb_client_secrets.json`
```
{
  "web": {
    "api_key": "xxxx",
    "app_secret": "xxxxx"
  }
}
```


#### Google
`client_secrets.json`
```
{
    "web": {
        "client_id":"xxxxxx.apps.googleusercontent.com",
        "project_id":"xxxx",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"xxxxxxxx",
        "redirect_uris":["http://www.example.com/oauth2callback"],"javascript_origins":["http://localhost:5000"]
    }
}
```


#### Last.fm
`last.json`
```
{
  "web": {
    "api_key": "xxxx",
    "app_secret": "xxxxx"
  }
}
```


### Dependencies
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

5.  Install Modules in the virtual desktop environment:
Navigate the terminal to the project folder, then use command the following commands to start the virtual desktop environment:
```
$ vagrant up
$ vagrant ssh
```

While in the virtual desktop environment, use the following `sudo` commands to install dependencies:
```
vagrant@precise32:~$   sudo apt-get install libffi-dev libssl-dev
vagrant@precise32:~$   sudo pip install requests[security] --upgrade
```


### Running The App Locally
In order to run the app locally, `vagrant` must be installed on your system (see above), and your project folder must include the `Vagrantfile` and `pf_config.sh` files in the top level of your project folder.

Navigate the terminal to the project folder, and use the following commands to start the start virtual environment and run the app.
```
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ python main.py
```
Point your browser to `localhost:5000` to view the app.


### What's included
Within the project folder, you will find the following files:

```
catalog/
    ├── static/
    |    ├── code-break/
    |    ├── js/
    |    |    └── main.js
    |    └── css/
    |         └── styles/
    |               ├── main.css
    |               └── media.css
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
    ├── .gitignore
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
    ├── todo_list.txt
    ├── Song.py
    ├── User.py
    └── Vagrantfile
```

## Creator

**Ian Agpawa**

 agpawaji@gmail.com
