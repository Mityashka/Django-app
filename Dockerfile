FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /django-app

COPY siteek/requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY siteek .

CMD ["gunicorn", "siteek.wsgi:application", "--bind", "0.0.0.0:8000"]