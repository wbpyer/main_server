from flask import Flask
from flask_caching import Cache



config = {

    "DEBUG": True,          # some Flask specific configs

    "CACHE_DEFAULT_TIMEOUT": 300,
'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': '172.16.13.1',
  'CACHE_REDIS_PORT': 6379,
  'CACHE_REDIS_DB': '0',
   'CACHE_REDIS_PASSWORD': ''


}

app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


#创建缓存视图函数
@app.route('/')
#timeout:指定缓存有效期，默认为300s
#key_prefix:缓存键前缀,默认为 view/ +路由地址
@cache.cached(timeout=10000,key_prefix='index')
def set_cache():
    #进行测试,第一次时会执行,之后就会直接调用缓存数据
    print('调动数据库')
    return '返回结果'



@app.route('/set')
def set_cache3():
    #先去缓存中查找数据
    data = cache.get('data')

    #如果缓存中有数据,返回缓存数据
    if data:
        print('缓存数据')
        return data

    #如果缓存中没有数据,设置新数据
    data = '123456'

    #并在缓存中设置
    cache.set('data',data,timeout=100)

    print('非缓存数据')

    return data





if __name__  == "__main__":
    app.run('0.0.0.0',9000)