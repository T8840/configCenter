"""app模块，包含app工厂功能"""
import json
from flask import Flask, render_template, jsonify, send_from_directory

from App import commands
from App.extensions import bcrypt, cache, cors, db, migrate, debug_toolbar, apispec
# 此处从urls导入是为了restful能正常加载到url设置
from App.urls import blueprint
# 导入日志配置
from App.settings import dictConfig

from pubCode.pubUtils.configReader import GetCnf
from pubCode.pubEnums.flaskResEnum import ResCode
from pubCode.flaskExts.customError import CustomBuzz
from pubCode.pubUtils.jsonExtend import CustomEncoder

def createApp(configObject='App.settings'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(configObject)
    # app.logger.info(f"系统启动配置如下:\n {json.dumps(app.config, indent=4, ensure_ascii=False, cls=CustomEncoder)}")
    registerExtensions(app)
    registerBlueprints(app)
    registerErrorhandlers(app)
    registerShellcontext(app)
    registerCommands(app)
    configure_apispec(app)
    # initCustomConfig(app)
    return app

def addFavicon(app):
    """
    添加favicon
    :param app:
    :return:
    """
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('../Static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


def registerExtensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app)
    debug_toolbar.init_app(app)
    return None


def registerBlueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blueprint)
    return None

def registerErrorhandlers(app):
    """Register error handlers."""

    def customError(error):
        app.logger.exception(error)
        return (error.jsonify(), 200)

    def globalError(error):
        """global error return."""
        # If a HTTPException, pull the `code` attribute; default to 500
        app.logger.exception("globalError")
        app.logger.exception(error)
        errorCode = getattr(error, "code", 500)
        # 自定义 abort 中通过 description 传入参数
        errorDesc = getattr(error, "description", {})
        respCode, respMsg, respData = [None] * 3
        # 处理自定义 abort 错误逻辑
        if errorDesc and isinstance(errorDesc, dict):
            respCode = errorDesc.get("code")
            respMsg = errorDesc.get("msg")
            respData = errorDesc.get("data")

        # 处理不存在的url
        elif errorCode == 404:
            respCode = ResCode.NOT_FOUND
            respMsg = "请求的url不在支持范围内~请确认url!"
            respData = {}
        try:
            data = error.description
        except AttributeError:
            data = repr(error)
        return (
            jsonify(
                {
                    "code": respCode or "999999",
                    "msg": respMsg or "系统异常!",
                    "data": data if respData is None else respData,
                }
            ),
            errorCode,
        )

    # 注册自定义异常捕获方法
    app.errorhandler(CustomBuzz)(customError)
    # 注册全局http code异常捕获方法
    for errcode in [401, 403, 404, 405, 500, 501, 503]:
        app.errorhandler(errcode)(globalError)
    return None


def registerShellcontext(app):
    """
        Register shell context objects.
        新增的数据库model需要增加到这里
    """
    def shellContext():
        """Shell context objects."""
        return {'db': db}
    app.shell_context_processor(shellContext)


def registerCommands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)

def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app)
    # apispec.init_app(app, security=[{"jwt": []}])
    # apispec.spec.components.security_scheme(
    #     "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    # )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )

def initCustomConfig(app):
    """
    初始化所需配置信息
    通过写入 app.config 中的自定义 customConfig key实现
  """
    app.config.update(
        {
            "customConfig": {
                "dbConf": {
                    "Test1": GetCnf.dbInfo("Test1"),
                    "Test2": GetCnf.dbInfo("Test2"),
                    "Test3": GetCnf.dbInfo("Test3"),
                    "Test4": GetCnf.dbInfo("Test4"),
                    "Test5": GetCnf.dbInfo("Test5"),
                    "Test6": GetCnf.dbInfo("Test6"),
                },
                "rabbitConf": GetCnf.rabbitMqInfo('rabbitMQ_156'),
                "redisConf": GetCnf.redisInfo("Tester_156")
            }
        }
    )
