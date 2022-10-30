FROM python:3.10

EXPOSE 5000
WORKDIR /app


COPY requirements.txt /app
COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python app.py
