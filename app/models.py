from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash


# python manager.py db init
# python manager.py db migrate
# python manager.py db upgrade
class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class User(BaseModel, db.Model):
    """用户"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # 用户与房屋 一对多
    house_list = db.relationship("House", backref="user")

    # order = db.relationship("Order", backrel="user")

    # 加上property装饰器后，会把函数变为属性，属性名即为函数名
    @property
    def password(self):
        """读取属性的函数行为"""
        # return self.password_hash
        raise AttributeError("这个属性只能设置，不能读取")  # raise 手动抛出异常

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)


# 房屋与设施中间表，多对多关系
house_facility = db.Table(
    "m_house_facility",
    db.Column("house_id", db.Integer, db.ForeignKey("house.id"), primary_key=True),  # 联合主键
    db.Column("facility_id", db.Integer, db.ForeignKey("facility.id"), primary_key=True)  # 联合主键

)


class House(BaseModel, db.Model):
    """房子"""

    __tablename__ = "house"

    id = db.Column(db.Integer, primary_key=True)
    # 一对多对应的一的外键
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    # 多对多用secondary进行二次查询
    facility_list = db.relationship("Facility", secondary=house_facility)


class Facility(BaseModel, db.Model):
    """设施"""

    __tablename__ = "facility"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
