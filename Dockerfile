FROM python:3.8-slim-buster

WORKDIR /examples

COPY ./requirements.txt /examples
RUN pip3 install -r requirements.txt

COPY . .  


EXPOSE 5000
ENV FLASK_APP=examples/example3_exercises.py
CMD ["flask", "run", "--host=0.0.0.0"]
