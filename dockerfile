FROM python:3.12.2-slim

LABEL manteiner = "mantelo"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/usr/local

WORKDIR /app/

COPY . .


RUN  pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd \
    && cd /etc/ssh/ \
    && ssh-keygen -A

RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /app/init_container.sh && \
    chmod +x /app/init_container.sh 

COPY sshd_config /etc/ssh/

EXPOSE 8910 5000

ENTRYPOINT ["bash", "init_container.sh" ]