FROM python:3.10

COPY . /app
WORKDIR /app
RUN pip install --no-cache --upgrade pip
RUN pip install -r requirements.txt
ENV ENV=PROD
ENV PYTHONPATH=/app:$PYTHONPATH
ENV FLASK_ENV=production
EXPOSE 8000
CMD gunicorn --workers=2 --threads=4 --bind=0.0.0.0:8000 src.main:app