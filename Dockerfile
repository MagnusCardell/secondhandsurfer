FROM python:3
ADD server /server
WORKDIR /server
RUN pip install -r requirements.txt
COPY . /
CMD python app.py