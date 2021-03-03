from config.secret_config import SERVER_PORT, SERVER_HOST, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

SERVER_INFO = {
    'port': SERVER_PORT,
    'host': SERVER_HOST,
    'debug': False,
}

REDIS_INFO = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': REDIS_DB,
    'password': REDIS_PASSWORD,
    'decode_responses': True
}
