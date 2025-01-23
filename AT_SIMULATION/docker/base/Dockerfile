FROM python:3.10

WORKDIR /src

RUN apt-get update && \
    apt-get install -y wget && \
    wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz && \
    rm go1.23.4.linux-amd64.tar.gz && \
    ln -s /usr/local/go/bin/go /usr/bin/go && \
    curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b /usr/local/bin latest && \
    /usr/local/go/bin/go install golang.org/x/tools/cmd/goimports@latest && \
    pip install poetry && \
    poetry config virtualenvs.create false

ENV PATH=$PATH:/root/go/bin

COPY pyproject.toml poetry.lock /src/

RUN poetry install --no-root

COPY . .

RUN chmod +x ./src/start.sh

CMD ["./src/start.sh"]
