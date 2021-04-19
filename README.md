# Запуск проекта

Для запуска проекта необходимо запустить отдельные сервисы в том порядке, в котором они находятся в этом описании.

### Запуск кластера kafka

    cd db/kafka
    docker-compose up -d

### Запуск API
    
    cd kafka-api
    docker-compose up -d

Документация к API: http://0.0.0.0:8888/api/openapi#/

### Запуск ClickHouse

    cd db/clickhouse
    docker-compose up -d
    
### Запуск ETL
    
    cd etl
    docker-compose up -d


После успешного запуска всех сервисов можно отправлять post-запросы в API и эти данные окажутся в базе CLickHouse.
