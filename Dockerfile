FROM python:3
ENV PYTHONUNBUFFERED 1

# setup working directory
RUN mkdir /code
WORKDIR /code
ADD . /code

RUN pip install --upgrade pip
RUN pip uninstall psycopg2
RUN pip install --upgrade wheel
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

RUN ["chmod", "+x", "./scripts/wait_for_postgres.sh"]
RUN ["chmod", "+x", "./scripts/start-django.sh"]