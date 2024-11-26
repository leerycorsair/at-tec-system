FROM python:3.10

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .

RUN chmod +x ./src/start.sh

CMD ["./src/start.sh"]
