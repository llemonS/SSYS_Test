FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
EXPOSE 8080
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/