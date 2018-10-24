## Local

Setup db and run server

    <!-- export TEST_URL=http://localhost
    export REACT_APP_USERS_SERVICE_URL=http://localhost:5000
    export REACT_APP_ELASTICSEARCH_IP=http://elasticsearch:9200 -->

    docker-compose up -d --build
    docker-compose run server python3 manage.py recreate_db
    docker-compose run server python3 manage.py seed_db
    docker-compose run server python3 manage.py test

    python3 manage.py recreate_db
    python3 manage.py seed_db
    python3 manage.py test

# Fix Server

    export APP_SETTINGS=app.config.DevelopmentConfig
    export DATABASE_URL=postgres://postgres:postgres@al_db:5432/active_learner

    docker run -itv $PWD:/usr/src/app activelearner_server /bin/bash
