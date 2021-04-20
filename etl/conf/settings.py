import os
import yaml
from pathlib import Path


CH_HOST = os.environ.get('CH_HOST', default='clickhouse://clickhouse-node1')
CH_TABLE = os.environ.get('CH_TABLE', default='analysis.viewed_progress')

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', default='views')
KAFKA_CONSUMER_GROUP = os.environ.get('KAFKA_CONSUMER_GROUP', default='echo-messages-to-stdout')
KAFKA_SERVERS = os.environ.get('KAFKA_SERVERS', default=['localhost:9092', 'broker:29092'])

FLUSH_SECONDS = float(os.environ.get('FLUSH_SECONDS', default='30'))
FLUSH_COUNT = int(os.environ.get('FLUSH_COUNT', default='1000'))

# инициализируем конфиг для logging
path_log_conf = Path(__file__).parent.joinpath("log_conf.yaml")
with path_log_conf.open("r") as f:
    log_conf = yaml.safe_load(f)
