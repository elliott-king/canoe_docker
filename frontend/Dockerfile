# Use an official node runtime as a parent image
FROM node:12

WORKDIR /app

# Install dependencies
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock

RUN yarn install

# Add rest of the client code
COPY . /app

EXPOSE 3000

CMD yarn start