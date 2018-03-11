FROM python:3.4-alpine
MAINTAINER Juan Pedro Torres "juanp.95.torres@gmail.com"
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "avisos.py"]
