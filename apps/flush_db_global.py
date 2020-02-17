import redis

rdp_local = redis.ConnectionPool(host='127.0.0.1', port=6379, db=7)
rdc_local = redis.StrictRedis(connection_pool=rdp_local)


def fluash_redis():
    rdc_local.flushdb()


if __name__ == '__main__':
    rdc_local.flushdb()
