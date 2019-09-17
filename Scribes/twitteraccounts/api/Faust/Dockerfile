# FROM python:3.7-slim
    
# RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list \
#     && apt-get update \
#     && apt-get install -y --no-install-recommends apt-utils

# ENV PIP_FORMAT=legacy
# ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# RUN apt-get install -y netcat && apt-get autoremove -y

# # Create unprivileged user
# RUN adduser --disabled-password --gecos '' myuser 

# WORKDIR /faust/

# COPY . /faust

# RUN pip3 install -e .

# RUN ["chmod", "+x", "./wait_for_services.sh"]
# ENTRYPOINT ["./wait_for_services.sh"]

# RUN ["chmod", "+x", "./run.sh"]
# CMD ["./run.sh", "${WORKER}", "${WORKER_PORT}", "${CONFIG_CLASS}"]

FROM python:3.6.7

EXPOSE 9090

RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends apt-utils

ENV PIP_FORMAT=legacy
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get install -y netcat && apt-get autoremove -y

# Create unprivileged user
RUN adduser --disabled-password --gecos '' myuser 

WORKDIR /faust/

COPY . /faust

RUN pip3 install -e .
RUN pip install -r requirements.txt
RUN ["chmod", "+x", "./wait_for_services.sh"]
ENTRYPOINT ["./wait_for_services.sh"]

RUN ["chmod", "+x", "./run.sh"]
CMD ["./run.sh", "${WORKER}", "${WORKER_PORT}", "${CONFIG_CLASS}"]

# RUN mkdir /code
# WORKDIR /code
# COPY requirements.txt /code/

# COPY . .


# ENTRYPOINT run python daemon/app.py
# RUN ["chmod", "+x", "./run.sh"]
# CMD ["./run.sh", "${WORKER}", "${WORKER_PORT}", "${CONFIG_CLASS}"]