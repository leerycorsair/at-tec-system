FROM node:current-buster AS build-stage
WORKDIR /app/

COPY ./package* ./
RUN npm install

COPY . /app/
COPY ./.env /app/
 
RUN npm run build

FROM nginx:latest AS production-stage

COPY ./docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/build /usr/share/nginx/html
EXPOSE ${FRONTEND_PORT}
CMD ["nginx", "-g", "daemon off;"]