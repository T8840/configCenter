# 此模块是为了便于管理url 因此从views中引入api, blueprint，views

from App.api.views import api, blueprint
from App.api.views import ResfulHelloViews, \
                          CommonCnfViews, CommonCnfsViews, CommonCnfSearchViews, \
                          EnvCnfViews, EnvCnfsViews, EnvCnfSearchViews
from App.api.serializer import CommonCnfSchema , EnvCnfSchema
from App.extensions import apispec
from flask import current_app

api.add_resource(ResfulHelloViews, '/hello/<string:name>',endpoint="hello_by_name")

api.add_resource(CommonCnfViews, '/commonConfig/', '/commonConfig/<string:configKey>',endpoint="commonConfig_by_configKey")
api.add_resource(CommonCnfsViews, '/commonConfigs',endpoint="commonConfigs")
api.add_resource(CommonCnfSearchViews, '/commonConfigSearch',endpoint="commonConfigSearch")

api.add_resource(EnvCnfViews, '/envConfig/', '/envConfig/<string:env>/<string:configKey>',endpoint="envConfig_by_env_configKey")
api.add_resource(EnvCnfsViews, '/envConfigs',endpoint="envConfigs")
api.add_resource(EnvCnfSearchViews, '/envConfigSearch',endpoint="envConfigSearch")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=ResfulHelloViews, app=current_app)
    apispec.spec.path(view=CommonCnfViews, app=current_app)
    apispec.spec.path(view=EnvCnfViews, app=current_app)

    apispec.spec.components.schema("CommonCnfSchema", schema=CommonCnfSchema)
    apispec.spec.components.schema("EnvCnfSchema", schema=EnvCnfSchema)

