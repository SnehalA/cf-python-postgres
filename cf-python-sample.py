import os
import json
import psycopg2
import cherrypy

port = None
vcap = None
jdbc_uri = None
database_name = None
username = None
password_str = None
db_host = None
db_port = None
connected = False
conn = None
cur = None

### Application Configuration
portStr = os.getenv("VCAP_APP_PORT")

if portStr is not None:
    port = int(portStr)

services = os.getenv("VCAP_SERVICES")

if services is not None:
    vcap = json.loads(services)


if vcap is not None:
    postgres = vcap['postgresql93'][0]['credentials']  #changed from "postgresql"
    if postgres is not None:
        #jdbc_uri = postgres['jdbc_uri'] not avaialble in this env using uri instead
        uri=postgres['uri']
        database_name = postgres['dbname']
        username = postgres['username']
        password_str = postgres['password']
        db_host = postgres['hostname']
        db_port = postgres['port']
else:
    database_name = '<DATABASE_NAME>'
    username = '<USERNAME>'
    password_str = '<PASSWORD>'
    db_host = 'localhost'
    db_port = 5432

try:
    conn = psycopg2.connect(database=database_name, user=username, password=password_str, host=db_host, port=db_port)
    connected = True
    cur = conn.cursor()
except:
    connected = False


### APIs
class getData:
    ### users api - GET - retrieve users
    def GET(self, **kwargs):
        try:
            dataset=kwargs["frame"]
        except:
            dataset='sample.users'
        response = ''
        query = 'SELECT * FROM '+dataset
        print query
        if cur is not None:
            cur.execute(query)
            conn.commit()
            rows = cur.fetchall()
            response = json.dumps(rows)
        return response

class getDetails:
    exposed = True
       ### Main api - GET - provides connection info

    def GET(self, **kwargs):
        response = '<h1>Database Connection Info</h1><hr>'

        if uri is not None:
            response += '<b>jdbc_uri:</b> ' + uri + "<BR>"

        if database_name is not None:
            response += '<b>database:</b> ' + database_name + "<BR>"

        if username is not None:
            response += '<b>username:</b> ' + username + "<BR>"

        if password_str is not None:
            response += '<b>password:</b> ' + password_str + "<BR>"

        if db_host is not None:
            response += '<b>host:</b> ' + db_host + "<BR>"

        if db_port is not None:
            response += '<b>port:</b> ' + str(db_port) + "<BR>"

        response += '<hr>'

        if connected is True:
            response += '<font color="#00FF00"><b>Database connection is active</b></font>'
        else:
            response += '<font color="#FF0000"><b>Database is not connected</b></font>'

        return response

if __name__ == '__main__':

    print 'connected to postgres : ', connected

    cherrypy.tree.mount(
        getDetails(), '/',
        {'/':
             {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
              'tools.sessions.on': True,
              'tools.response_headers.on': True,
              'tools.response_headers.headers': [('Content-Type', 'text/html')],
              'tools.gzip.on': True
              }
         }
    )
    cherrypy.tree.mount(
        getData(), '/data',
        {'/':
             {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
              'tools.sessions.on': True,
              'tools.response_headers.on': True,
              'tools.response_headers.headers': [('Content-Type', 'application/json')],
              'tools.gzip.on': True
              }
         }
    )
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.engine.start()
    cherrypy.engine.block()

