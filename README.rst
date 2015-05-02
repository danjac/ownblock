========================
ownblock
========================

Community management application for apartment blocks and condos. Written in Django ad AngularJS.

========================
requirements
========================

* Python 3
* PostgreSQL
* Bower

========================
installation
========================

    cd ownblock/

    pip install -r ../requirements/local.txt

    npm install 

    gulp

Create a new database in PostgreSQL:

    createdb -U <name> -W <db_name>

Set the following environment variables to point to your database:
    
    DJANGO_DB_NAME

    DJANGO_DB_USER

    DJANGO_DB_PASSWORD

Run migrations:
    
    python manage.py migrate 

Online demo: http://demo.ownblock.com

