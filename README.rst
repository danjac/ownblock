========================
ownblock
========================

Community management application for apartment blocks and condos. Written in Django ad AngularJS.

========================
requirements
========================

Python 3
PostgreSQL
Bower

========================
installation
========================

    pip install -r requirements.txt
    bower install 

Set the following environment variables:
    
    DB_NAME
    DB_USER
    DB_PASSWORD

Run migrations:
    
    python ownblock/manage.py migrate 

Online demo: http://demo.ownblock.com

