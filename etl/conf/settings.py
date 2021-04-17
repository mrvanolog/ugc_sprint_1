import os


CH_HOST = os.environ.get('CH_HOST', default='localhost')
CH_TABLE = os.environ.get('CH_TABLE', default='analysis.viewed_progress')

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP = os.environ.get('KAFKA_CONSUMER_GROUP')
KAFKA_SERVERS = os.environ.get('KAFKA_SERVERS')

FLUSH_SECONDS = float(os.environ.get('FLUSH_SECONDS', default='30'))
FLUSH_COUNT = int(os.environ.get('FLUSH_COUNT', default='1000'))
