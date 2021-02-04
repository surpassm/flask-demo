# coding:utf-8

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_map
from logging.handlers import RotatingFileHandler

import logging
import redis

# 数据库
db = SQLAlchemy()

# 创建Redis对象
redis_store = None

# 为flask补充csrf防护机制
csrf = CSRFProtect()

logging.basicConfig(level=logging.DEBUG)
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 50, backupCount=10)
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    """
    创建flask应用对象
    :param config_name : str 开发模式 {'dev'、'prod'}
    :return app
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 数据库：使用app初始化db
    db.init_app(app)

    # 初始化Redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_PORT, port=config_class.REDIS_HOST)
    # 利用flask-session，将session数据保存到Redis中
    Session(app)
    # 为flask补充csrf防护
    csrf.init_app(app)

    # 注册蓝图
    from . import api_v1
    app.register_blueprint(api_v1.api, url_prefix="/api/v1.0")

    return app
