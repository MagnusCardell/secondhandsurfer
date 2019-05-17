FROM python:3
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
COPY . /app
ENV PATH /app:$PATH
CMD ["gunicorn","--config","/app/gunicorn_config.py","app:app"]

EXPOSE 8080
