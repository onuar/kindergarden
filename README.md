# HTTP server playground

# Development:
## gunicorn's garden: 
* cd gunicorns-garden
* virtualenv venv-guni -p python3
* source venv-guni/bin/activate
* pip install -r requirements.txt

## uwsgi's garden: 
* cd uwsgis-garden
* virtualenv venv-uwsgi -p python3
* source venv-uwsgi/bin/activate
* pip install -r requirements.txt

## werkzeug's garden: 
* cd werkzeugs-garden
* virtualenv venv-werk -p python3
* source venv-werk/bin/activate
* pip install -r requirements.txt

##  tornado's garden: 
* cd tornados-garden
* virtualenv venv-tor -p python3
* source venv-tor/bin/activate
* pip install -r requirements.txt

# Docs:
* gunicorn: https://github.com/benoitc/gunicorn
* uwsgi: https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html
* werkzeug: http://werkzeug.pocoo.org/
* tornado: https://github.com/tornadoweb/tornado