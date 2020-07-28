# -*- coding:utf-8 -*-
#  api 视图类
from flask import Blueprint, render_template, jsonify , current_app as app
from flask_restful import Api, Resource, reqparse

#  导入工具类
from App.utils import removeNoneKey, strToJson, jsonToStr, paginateParams
from pubCode.pubUtils.msgBuilder import MsgBuilder
from pubCode.pubEnums.flaskResEnum import ResCode
#
from App.api.models import db, CommonCnf, EnvCnf, SrvCnf
from App.api.serializer import CommonCnfSchema, EnvCnfSchema, SrvCnfSchema, TeamProjectSchema

blueprint = Blueprint(
    'api', __name__,
    url_prefix='/configCenter/api',
    static_folder='../../Static',
    static_url_path='/static')

api = Api(blueprint)

@blueprint.route('/hello')
def hello():
    return jsonify({
        'code': '000000',
        'succeed': True,
        'message': 'Hello World!!!'
    })

class ResfulHelloViews(Resource):

    def get(self, name):
        return jsonify({
            'code': '000000',
            'succeed': True,
            'message': f'Hello {name}!!!'
        })

commonCnfParams = reqparse.RequestParser()
commonCnfParams.add_argument("key", required=True, type=str,location=["json"])
commonCnfParams.add_argument("value", type=str, required=True,location=["json"])
commonCnfParams.add_argument("desc", type=str,location=["json"])
commonCnfParams.add_argument("active", default=True, type=bool, location=["json"])

class CommonCnfViews(Resource):
    """
        通用配置类单一视图
    """
    def get(self, configKey):
        """
        获取通用配置
        :param configKey: 通用配置的key
        :return:
        """
        app.logger.info(f"CommonCnfViews get(configKey={configKey})")
        msg = MsgBuilder()
        config = CommonCnf.query.filter_by(key=configKey).first()
        commonCnfSchema = CommonCnfSchema()
        configSerialized = commonCnfSchema.dump(config)
        msg.setSucceed(respData=configSerialized)
        return jsonify(msg.getMsg())

    def post(self):
        app.logger.info(f"CommonCnfViews post({commonCnfParams.parse_args()})")
        msg=MsgBuilder()
        args = removeNoneKey(commonCnfParams.parse_args())
        if CommonCnf.query.filter_by(key=args.get("key")).first():
            msg.setFailed(ResCode.UNIQUE_ERROR, msg=f'key={args.get("key")}已存在！')
        else:
            commonCnfSchema = CommonCnfSchema()
            # 因为 value字段可能是可能是单纯字符串,也可能是符合json格式的 此处不用schema.load而做特殊处理
            args["value"] =strToJson(args.get("value"))
            CommonCnf.create(**jsonToStr(args))
            res = CommonCnf.query.filter_by(key=args.get("key")).first()
            msg.setSucceed(respData=commonCnfSchema.dump(res))
        return jsonify(msg.getMsg())

    def put(self):
        app.logger.info(f"CommonCnfViews put({commonCnfParams.parse_args()})")
        msg = MsgBuilder()
        args = removeNoneKey(commonCnfParams.parse_args())
        key = args.get("key")
        cnf = CommonCnf.query.filter_by(key=key).first()
        if cnf:
            # 因为 value字段可能是可能是单纯字符串,也可能是符合json格式的 此处不用schema.load而做特殊处理
            args["value"] = strToJson(args.get("value"))
            cnf.update(**jsonToStr(args))
            res = CommonCnf.query.filter_by(key=args.get("key")).first()
            commonCnfSchema = CommonCnfSchema()
            msg.setSucceed(respData=commonCnfSchema.dump(res))
        else:
            msg.setFailed(ResCode.NOT_FOUND, msg=f'key={args.get("key")}不存在！')
        return jsonify(msg.getMsg())

    def delete(self,configKey):
        app.logger.info(f"CommonCnfViews delete(configKey={configKey})")
        msg = MsgBuilder()
        cnf = CommonCnf.query.filter_by(key=configKey).first()
        if cnf:
            cnf.update(active=0)
            res = CommonCnf.query.filter_by(key=configKey).first()
            commonCnfSchema = CommonCnfSchema()
            msg.setSucceed(respData=commonCnfSchema.dump(res))
        else:
            msg.setFailed(ResCode.NOT_FOUND, msg=f'key={configKey}不存在！')
        return jsonify(msg.getMsg())


class CommonCnfsViews(Resource):
    """
        通用配置类列表视图
    """
    def get(self):
        """
        获取通用配置
        :param
        :return: list
        """
        msg = MsgBuilder()
        config = CommonCnf.query.filter_by(active=1)
        commonCnfSchema = CommonCnfSchema(many=True)
        configSerialized = commonCnfSchema.dump(config)
        msg.setSucceed(respData=configSerialized)
        return jsonify(msg.getMsg())

commonCnfSelect = reqparse.RequestParser()
commonCnfSelect.add_argument("key", type=str, location=["args"])
commonCnfSelect.add_argument("value", type=str, location=["args"])
commonCnfSelect.add_argument("desc", type=str, location=["args"])
commonCnfSelect.add_argument("page", type=int, default=1, location=["args"])
commonCnfSelect.add_argument("limit", type=int, default=12, location=["args"])

class CommonCnfSearchViews(Resource):
    """
    通用配置类查询列表视图
    """
    def get(self):
        app.logger.info(f"CommonCnfSelectViews get(commonCnfSelect={commonCnfSelect.parse_args()}")
        msg = MsgBuilder()
        args = commonCnfSelect.parse_args()
        pageNum , limitNum = paginateParams(args)
        searchParams = []
        if args.get("key"):
            searchParams.append(CommonCnf.key.ilike(f'%{args.get("key")}%'))
        if args.get("value"):
            searchParams.append(CommonCnf.value.ilike(f'%{args.get("value")}%'))
        if args.get("desc"):
            searchParams.append(CommonCnf.desc.ilike(f'%{args.get("desc")}%'))
        total = CommonCnf.query.filter(db.and_(*searchParams)).count()
        commonCnfs = CommonCnf.query.filter(db.and_(*searchParams)).limit(limitNum).offset(pageNum)
        commonCnfSchema = CommonCnfSchema(many=True)
        msg.setSucceed(respData=commonCnfSchema.dump(commonCnfs))
        msg.addMsgField({"total":total})
        return jsonify(msg.getMsg())




envCnfParams = reqparse.RequestParser()
envCnfParams.add_argument("env", required=True, type=str,location=["json"])
envCnfParams.add_argument("key", required=True, type=str,location=["json"])
envCnfParams.add_argument("value", type=str, required=True,location=["json"])
envCnfParams.add_argument("desc", type=str,location=["json"])
envCnfParams.add_argument("active", default=True, type=bool, location=["json"])

class EnvCnfViews(Resource):
    """
        环境配置类单一视图
    """
    def get(self, env,configKey):
        """
        获取环境配置
        :param env:环境  configKey: 通用配置的key
        :return:
        """
        app.logger.info(f"EnvCnfViews get(env={env} configKey={configKey})")
        msg = MsgBuilder()
        config = EnvCnf.query.filter_by(env=env, key=configKey, active=1).first()
        envCnfSchema = EnvCnfSchema()
        configSerialized = envCnfSchema.dump(config)
        msg.setSucceed(respData=configSerialized)
        return jsonify(msg.getMsg())

    def post(self):
        app.logger.info(f"EnvCnfViews post({envCnfParams.parse_args()})")
        msg=MsgBuilder()
        args = removeNoneKey(envCnfParams.parse_args())
        if EnvCnf.query.filter_by(env=args.get("env"), key=args.get("key")).first():
            msg.setFailed(ResCode.UNIQUE_ERROR, msg=f'env={args.get("env")} key={args.get("key")}已存在！')
        else:
            envCnfSchema = EnvCnfSchema()
            # 因为 value字段可能是可能是单纯字符串,也可能是符合json格式的 此处不用schema.load而做特殊处理
            args["value"] =strToJson(args.get("value"))
            EnvCnf.create(**jsonToStr(args))
            res = EnvCnf.query.filter_by(env=args.get("env"), key=args.get("key")).first()
            msg.setSucceed(respData=envCnfSchema.dump(res))
        return jsonify(msg.getMsg())

    def put(self):
        app.logger.info(f"envCnfViews put({envCnfParams.parse_args()})")
        msg = MsgBuilder()
        args = removeNoneKey(envCnfParams.parse_args())
        key = args.get("key")
        env = args.get("env")
        cnf = EnvCnf.query.filter_by(env=env,key=key).first()
        if cnf:
            # 因为 value字段可能是可能是单纯字符串,也可能是符合json格式的 此处不用schema.load而做特殊处理
            args["value"] = strToJson(args.get("value"))
            cnf.update(**jsonToStr(args))
            res = EnvCnf.query.filter_by(env=args.get("env"),key=args.get("key")).first()
            envCnfSchema = EnvCnfSchema()
            msg.setSucceed(respData=envCnfSchema.dump(res))
        else:
            msg.setFailed(ResCode.NOT_FOUND, msg=f'env={args.get("env")} key={args.get("key")}不存在！')
        return jsonify(msg.getMsg())

    def delete(self, env, configKey):
        app.logger.info(f"envCnfViews delete(env={env} configKey={configKey})")
        msg = MsgBuilder()
        cnf = EnvCnf.query.filter_by(env=env, key=configKey).first()
        if cnf:
            cnf.update(active=0)
            res = EnvCnf.query.filter_by(env=env, key=configKey).first()
            envCnfSchema = EnvCnfSchema()
            msg.setSucceed(respData=envCnfSchema.dump(res))
        else:
            msg.setFailed(ResCode.NOT_FOUND, msg=f'key={configKey}不存在！')
        return jsonify(msg.getMsg())


class EnvCnfsViews(Resource):
    """
        环境配置类列表视图
    """
    def get(self):
        """
        获取环境配置
        :param
        :return: list
        """
        msg = MsgBuilder()
        config = EnvCnf.query.filter_by(active=1)
        envCnfSchema = EnvCnfSchema(many=True)
        configSerialized = envCnfSchema.dump(config)
        msg.setSucceed(respData=configSerialized)
        return jsonify(msg.getMsg())

envCnfSelect = reqparse.RequestParser()
envCnfSelect.add_argument("env", type=str, location=["args"])
envCnfSelect.add_argument("key", type=str, location=["args"])
envCnfSelect.add_argument("value", type=str, location=["args"])
envCnfSelect.add_argument("desc", type=str, location=["args"])
envCnfSelect.add_argument("page", type=int, default=1, location=["args"])
envCnfSelect.add_argument("limit", type=int, default=12, location=["args"])

class EnvCnfSearchViews(Resource):
    """
    通用环境类查询列表视图
    """
    def get(self):
        app.logger.info(f"EnvCnfSelectViews get(envCnfSelect={envCnfSelect.parse_args()}")
        msg = MsgBuilder()
        args = envCnfSelect.parse_args()
        pageNum , limitNum = paginateParams(args)
        searchParams = []
        if args.get("env"):
            searchParams.append(EnvCnf.key.ilike(f'%{args.get("env")}%'))
        if args.get("key"):
            searchParams.append(EnvCnf.key.ilike(f'%{args.get("key")}%'))
        if args.get("value"):
            searchParams.append(EnvCnf.value.ilike(f'%{args.get("value")}%'))
        if args.get("desc"):
            searchParams.append(EnvCnf.desc.ilike(f'%{args.get("desc")}%'))
        total = EnvCnf.query.filter(db.and_(*searchParams)).count()
        envCnfs = EnvCnf.query.filter(db.and_(*searchParams)).limit(limitNum).offset(pageNum)
        envCnfSchema = EnvCnfSchema(many=True)
        msg.setSucceed(respData=envCnfSchema.dump(envCnfs))
        msg.addMsgField({"total":total})
        return jsonify(msg.getMsg())



class SrvCnfViews(Resource):
    """
    服务配置单一视图：
        来源：发版平台
        功能：通过env+project -> projectInfo(Example: project IP and so on)
    """
    def get(self, env, project):
        """
        获取服务配置
        """
        app.logger.info(f"EnvCnfViews get(env={env} project={project})")
        msg = MsgBuilder()
        config = SrvCnf.query.filter_by(env=env, project=project, active=1).first()
        app.logger.info(f"EnvCnfViews get(config={config})")
        srvCnfSchema = SrvCnfSchema()
        configSerialized = srvCnfSchema.dump(config)
        msg.setSucceed(respData=configSerialized)
        return jsonify(msg.getMsg())



srvCnfReqData = reqparse.RequestParser()
srvCnfReqData.add_argument("env", type=str, location=["args", "json"])
srvCnfReqData.add_argument("team", type=str, location=["args", "json"])
srvCnfReqData.add_argument("project", type=str, location=["args", "json"])

class SrvCnfsViews(Resource):
    """
    服务配置类列表视图
    """

    def get(self):
        """
        获取服务配置列表
        :return:list
        """
        app.logger.info(f"SrvCnfsViews get({srvCnfReqData.parse_args()})")
        msg = MsgBuilder()
        args = removeNoneKey(srvCnfReqData.parse_args())
        config = SrvCnf.query.filter_by(active=1, **args).all()
        srvCnfSchema = SrvCnfSchema(many=True)
        configSerialized = srvCnfSchema.dump(config)
        msg.setSucceed(respData=configSerialized)
        return jsonify(msg.getMsg())


teamProjectParams = reqparse.RequestParser()
teamProjectParams.add_argument("team", type=str, required=True, location=["args"])
teamProjectParams.add_argument("env", type=str, required=True, location=["args"])

class TeamProjectViews(Resource):
    """
    项目组项目视图
    """

    def get(self):
        app.logger.info(f"TeamProjectViews get({teamProjectParams.parse_args()})")
        msg = MsgBuilder()
        args = removeNoneKey(teamProjectParams.parse_args())
        teamInfo = SrvCnf.query.filter_by(active=1, **args).all()
        teamInfoSchema = TeamProjectSchema(many=True)
        teamInfoSerialized = teamInfoSchema.dump(teamInfo)
        msg.setSucceed(respData=[project.get("project") for project in teamInfoSerialized])
        return jsonify(msg.getMsg())


class TeamSetViews(Resource):
    """
    项目组集视图
    """

    def get(self):
        msg = MsgBuilder()
        allTeam = SrvCnf.query.all()
        teamList = list(set([team.team for team in allTeam]))
        msg.setSucceed(respData=teamList)
        return jsonify(msg.getMsg())