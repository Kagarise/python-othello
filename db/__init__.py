from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config.secret_config

engine = create_engine(config.secret_config.MYSQL_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_app(app):
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from db.statistics import Statistics
    from db.record import Record
    Base.metadata.create_all(bind=engine)
