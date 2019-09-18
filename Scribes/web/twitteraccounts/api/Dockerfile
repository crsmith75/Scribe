FROM python:3.6.7

EXPOSE 9090

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# ENTRYPOINT faust -A Scribes_faust worker -l info