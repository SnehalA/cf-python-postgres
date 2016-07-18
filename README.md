# CF Python Sample Application
A sample Cloud Foundry application written in Python using Flask and psycopg

## Getting Started
This application requires the following python modules:

[Flask](http://flask.pocoo.org/docs/0.10/quickstart)

[psycopg2](http://initd.org/psycopg/)

They can be installed by using the following commands

```bash
pip install flask

pip install psycopg2
```

## Run Locally
To run the application locally, you must run a local instance of postgres.

Please run sample_db.sql on your local instance to create the sample table

Please replace the following strings in cf-python-sample.py with your local credentials

```bash
database_name = '<DATABASE_NAME>'
username = '<USERNAME>'
password_str = '<PASSWORD>'
```

The application can be run locally with the command

```bash
python cf-python-sample.py
```

There are is only a single api

```bash
/users
```

## Run on Cloud Foundry
Please create an instance of postgres called *sample-db* in your Cloud Foundry space.

To push the application, use the following command:

```bash
cf push -f manifest
```

To see the results, point your browser to
```bash
http://cf-python-sample.<cf target>/users
```