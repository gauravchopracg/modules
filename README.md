# modules

This repository contains files on a Overlook web application which is currently in stage of development.

Live web app is here:
[Website](http://todomagic.herokuapp.com/)


# Building the web application

Web application has been developed with Python and Flask framework. The project has been developed using the tutorial [Flask Mega-Tutorial for Python 3.6](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

**To run the app in you computer:**

1. Clone the repo

```bash
git clone https://github.com/gauravchopracg/modules.git
cd modules/
```

2. Create and activate virtual environment
```bash
virtualenv venv
venv\Scripts\activate
```

3. Modify Requirements and Install Dependencies

Remove gunicorn and psycopg2 from requirements.txt, since they are for development servers and install dependencies without them.

```bash
pip install -r requirements.txt
```

4. Config variables in .flaskenv file to support email functionalities
* FLASK_APP=todomagic.py
* MAIL_SERVER=smtp.googlemail.com
* MAIL_PORT=587
* MAIL_USE_TLS=1
* MAIL_USERNAME=########@gmail.com
* MAIL_PASSWORD=#####

5. Create migration repository

```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run and play with it

```bash
flask run
```


# Deployment on heroku

To deploy the application on the Heroku

1. Creating Heroku account

Go to heroku.com and create a free account.

2. Installing the Heroku CLI

Heroku provides a command-line tool for interacting with their service called Heroku CLI, available for Windows, Mac OS X and Linux. The documentation includes installation for all the supported platforms. Go ahead and install it on your system.

After that you should login to your Heroku account:

```bash
heroku login
```

3. Setting Up Git

To deploy application to Heroku, you must have git tool installed on your system. If you don't have it yet, you can visit the git site to download an installer.

After that you can clone the application from Github:

```bash
git clone https://github.com/gauravchopracg/modules.git
cd modules
```

4. Creating a Heroku Application

```bash
heroku apps:create Overlook
```

to check the URL that Heroku assigned to the application run git remote command:

```bash
git remote -v
```

5. Switch to Heroku Postgres Database

Heroku has a database offering of its own, based on the Postgres database, so I'm going to switch to that:

```bash
heroku addons:add heroku-postgresql:hobby-dev
```

6. Configuring variables

Heroku CLI makes easier to set environment variables to be used at runtime:
```bash
heroku config:set LOG_TO_STDOUT=1
heroku config:set FLASK_APP=todomagic.py
heroku config:set MAIL_SERVER=smtp.googlemail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=1
heroku config:set MAIL_USERNAME=########@gmail.com
heroku config:set MAIL_PASSWORD=#####
```

### Note: Updates to Requirements

Heroku expects the dependencies to be in the requirements.txt file, in your computer you can remove extra dependencies added in the requirements.txt file gunicorn and psycopg2. Since Heroku does not provide a web server of its own. Instead it expects the application to start its own web server on the port number given in the environment variable $PORT. Since the Flask development web server is not robust enough to use for production, I'm using gunicorn again, the server recommended by Heroku for Python applications. The applications will also be connecting to a Postgres database, and for that SQLAlchemy requires the psycopg2 package to be installed.