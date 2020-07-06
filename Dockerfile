FROM python:3.8.2-slim-buster

EXPOSE 8000

WORKDIR /usr/src/app

RUN mkdir data

COPY requirements/main.txt requirements/main.txt

RUN pip install -r requirements/main.txt

COPY . .

CMD ["gunicorn", "superlists.wsgi"]