"""
应用程序配置。
大多数配置是通过环境变量设置的
对于本地开发，使用.env文件设置环境变量
"""
import os
from environs import Env
from logging.config import dictConfig

env = Env()
env.read_env()


#  环境参数 默认为production
ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
PORT = env.int("PORT", default=5000)
FLASK_PORT = env.int("FLASK_PORT", default=5000)

#  数据库连接地址
#  sqlite:////tmp/test.db
#  mysql+pymysql://username:password@server/db  指定通过pymysql驱动访问数据库
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")

#  项目密钥
SECRET_KEY = env.str("SECRET_KEY")

# 启用异常传播以自行处理
PROPAGATE_EXCEPTIONS = True

#  加解密日志
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)

DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False

#  缓存类型
CACHE_TYPE = "simple"  # Can be "simple", "memcached", "redis", etc.

# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", default=False)

# json串包含中文
JSON_AS_ASCII = env.bool("JSON_AS_ASCII", default=False)


# 日志配置
if os.path.exists("logs/"):
    pass
else:
    os.mkdir("logs/")

LOGGING = dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"simple": {"format": "%(asctime)s-%(name)s[%(filename)s:%(lineno)d]%(levelname)s: %(message)s"}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "debugHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "logs/debug.log",
                "maxBytes": 1024 * 1024 * 50,  # 日志大小 50M
                "backupCount": 5,
                "encoding": "utf8",
            },
            "infoHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "logs/info.log",
                "maxBytes": 1024 * 1024 * 50,  # 日志大小 50M
                "backupCount": 5,
                "encoding": "utf8",
            },
            "errorHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "logs/errors.log",
                "maxBytes": 1024 * 1024 * 50,  # 日志大小 50M
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {"flaskApp": {"level": "ERROR", "handlers": ["console"], "propagate": "no"}},
        "root": {"level": "INFO", "handlers": ["console", "debugHandler", "infoHandler", "errorHandler"]},
    }
)
