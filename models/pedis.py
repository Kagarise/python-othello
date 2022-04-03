import redis

from config.app_config import REDIS_INFO

pool = redis.ConnectionPool(**REDIS_INFO)
redis_client = redis.Redis(connection_pool=pool)


# 判断name是否存在
def r_list_exists(name):
    return redis_client.exists(name)


# 根据length创建list
def r_list_create(name, length):
    pipe = redis_client.pipeline()
    for idx in range(length):
        pipe.rpush(name, "")
    pipe.execute()


# 根据index设置value
def r_list_set(name, index, value):
    return redis_client.lset(name, index, value)


# 获取整个list
def r_list_get_all(name):
    return redis_client.lrange(name, 0, -1)


# 根据下表获取元素
def r_list_get_idx(name, idx):
    return redis_client.lindex(name, idx)

# 清空list
def r_list_clear(name):
    redis_client.ltrim(name, 1, 0)

# set取得成员所有信息
# def r_set_get(name):
#     return list(redis_client.smembers(name))


# set判断成员是否在集合中
# def r_set_count(name, value):
#     return redis_client.sismember(name, value)


# set追加值
# def r_set_add(name, value):
#     redis_client.sadd(name, value)


# set重新赋值
# def r_set_set(name, values):
#     pipe = redis_client.pipeline()
#     pipe.delete(name)
#     for value in values:
#         pipe.sadd(name, value)
#     pipe.execute()


# set删除值或删除整个set
# def r_set_remove(name, value=None):
#     if value is None:
#         redis_client.delete(name)
#     else:
#         redis_client.srem(name, value)
