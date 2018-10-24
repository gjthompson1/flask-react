FROM node:10

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install and cache app dependencies
ADD package.json /usr/src/app/package.json

RUN npm install -g yarn
RUN yarn --cwd /usr/src/app/ install

# start app
CMD ["npm", "start"]
