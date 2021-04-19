import time
from typing import Tuple
from clickhouse_driver import Client
from clickhouse_driver.errors import Error


# connect to db
def connection() -> Tuple[Client]:
    while True:
        try:
            node_1 = Client('clickhouse-node1')
            node_3 = Client('clickhouse-node3')
            return node_1, node_3
        except Error as e:
            print(e)
            print("Still trying to connect")
            time.sleep(1)


def init_node_1(client: Client):
    client.execute('CREATE DATABASE analysis;')
    client.execute('CREATE DATABASE shard;')
    client.execute('CREATE DATABASE replica;')
    client.execute(
        """
        CREATE TABLE shard.viewed_progress (
            `user_id` String,
            `movie_id` String,
            `viewed_frame` UInt64,
            `created_at` DateTime
        ) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/viewed_progress', 'replica_1')
        PARTITION BY toYYYYMMDD(created_at)
        ORDER BY created_at;
        """
    )
    client.execute(
        """
        CREATE TABLE replica.viewed_progress (
            `user_id` String,
            `movie_id` String,
            `viewed_frame` UInt64,
            `created_at` DateTime
        ) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/viewed_progress', 'replica_2')
        PARTITION BY toYYYYMMDD(created_at)
        ORDER BY created_at;
        """
    )
    client.execute(
        """
        CREATE TABLE analysis.viewed_progress (
            `user_id` String,
            `movie_id` String,
            `viewed_frame` UInt64,
            `created_at` DateTime
        ) ENGINE = Distributed('company_cluster', '', viewed_progress, rand());
        """
    )


def init_node_3(client: Client):
    client.execute('CREATE DATABASE analysis;')
    client.execute('CREATE DATABASE shard;')
    client.execute('CREATE DATABASE replica;')
    client.execute(
        """
        CREATE TABLE shard.viewed_progress (
            `user_id` String,
            `movie_id` String,
            `viewed_frame` UInt64,
            `created_at` DateTime
        ) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/viewed_progress', 'replica_1')
        PARTITION BY toYYYYMMDD(created_at)
        ORDER BY created_at;
        """
    )
    client.execute(
        """
        CREATE TABLE replica.viewed_progress (
            `user_id` String,
            `movie_id` String,
            `viewed_frame` UInt64,
            `created_at` DateTime
        ) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/viewed_progress', 'replica_2')
        PARTITION BY toYYYYMMDD(created_at)
        ORDER BY created_at;
        """
    )
    client.execute(
        """
        CREATE TABLE analysis.viewed_progress (
            `user_id` String,
            `movie_id` String,
            `viewed_frame` UInt64,
            `created_at` DateTime
        ) ENGINE = Distributed('company_cluster', '', viewed_progress, rand());
        """
    )


if __name__ == '__main__':
    print('connecting')
    node_1, node_3 = connection()
    print('init node 1')
    init_node_1(node_1)
    print('init node 3')
    init_node_3(node_3)
    print('success')
