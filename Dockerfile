FROM tiangolo/uwsgi-nginx-flask:python3.6

WORKDIR /app

ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV=development

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app

CMD ["flask", "run"]
