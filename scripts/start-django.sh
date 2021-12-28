cd Uks
# uncomment this to use sqlite as test db
#export UKS_TEST_DB=ON
# collect static files and put inside ./static/
python manage.py collectstatic --noinput
# setup db
python manage.py makemigrations
python manage.py migrate
# run Django develop server
#python3 manage.py runserver 0.0.0.0:8000
# run Django app inside gunicorn
# always use more than 1 worker
gunicorn --workers=3 Uks.wsgi -b 0.0.0.0:8000