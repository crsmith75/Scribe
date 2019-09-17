FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
# FROM python:3.6.7

# EXPOSE 9090

# RUN mkdir /code
# WORKDIR /code
# RUN pip3 install pipenv
# # RUN pipenv shell
# RUN pip install -r requirements.txt
# # RUN pipenv lock
# # RUN pipenv sync

# COPY . /code/

# RUN ["chmod", "+x", "./commands.sh"]
# ENTRYPOINT ["./commands.sh"]

# ENTRYPOINT run Scribes runserver 0.0.0.0:8000