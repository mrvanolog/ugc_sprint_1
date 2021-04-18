Запуск кластера kafka

    cd db/kafka
    docker-compose up -d

После запуска, проверить, что все сервисы стартовали

    docker-compose ps

Запуск API
    
    cd kafka-api
    docker-compose up -d

Swagger 

    http://0.0.0.0:8888/api/openapi#/