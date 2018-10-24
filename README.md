# Flask + React

This is a boiler plate template for flask and react (specifically create-react-app `CRA`)

Docker containers:

  - Server (flask)
  - Client (react - CRA)
  - Database (postgres)

Features:

  - hot-reloading for both client and server
  -

## Setup

Requirements:

  - linux (might work on windows I don't know).
  - docker

To run and build

    docker-compose up -d --build

To setup database

    docker-compose run server python manage.py db_setup

### Liveness

To check server is runnning:

    http://localhost:5000/ping

Should return:

```
{
  "message": "pong!!",
  "status": "success"
}
```

To check client is running:

    http://localhost:3001

Should show the client
