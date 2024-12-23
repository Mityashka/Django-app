FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /django-app

RUN pip install --upgrade pip "poetry==1.8.4"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY siteek .

CMD ["gunicorn", "siteek.wsgi:application", "--bind", "0.0.0.0:8000"]