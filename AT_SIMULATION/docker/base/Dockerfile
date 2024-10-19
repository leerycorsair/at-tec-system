FROM node:current-buster AS build-stage
WORKDIR /app/

COPY ./frontend/package* ./
RUN npm install

COPY ./frontend /app/
 
RUN npm run build

FROM python:3.10 AS server

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .
COPY --from=build-stage /app/build /src/frontend/build

RUN chmod +x ./src/start.sh

CMD ["./src/start.sh"]
