FROM python:3.10

WORKDIR /src

RUN apt-get update && \
    apt-get install -y wget && \
    wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz && \
    rm go1.23.4.linux-amd64.tar.gz && \
    ln -s /usr/local/go/bin/go /usr/bin/go && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /src/

RUN poetry install --no-root

COPY . .

RUN chmod +x ./src/start.sh

CMD ["./src/start.sh"]
