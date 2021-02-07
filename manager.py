from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 创建flask应用对象
app = create_app("dev")

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()


# pip freeze > requirements.txt
# python manager.py runserver

# 阿里支付第三方tools :https://github.com/fzlee/alipay pip install




