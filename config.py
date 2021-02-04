# coding:utf-8
import redis
import os


class Config(object):
    """配置信息"""

    SECRET_KEY = os.urandom(24)

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/flask-demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # REDIS
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中session_id 进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据有效期，单位秒


class DevelopmentConfig(Config):
    """开发模式"""
    DEBUG = True


class ProductConfig(Config):
    """线上环境"""
    pass


config_map = {
    "dev": DevelopmentConfig,
    "prod": ProductConfig
}
