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

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志的保存路径，每个日志文件的最大大小，保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式 等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（current_app）添加日志记录器
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
