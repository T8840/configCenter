"""辅助工具和装饰器"""
import copy
import json
import arrow
import random
import flask_restful
from json import JSONDecodeError

from flask import flash, abort
from flask_sqlalchemy import DefaultMeta

from App.database import Model
from pubCode.pubUtils.msgBuilder import MsgBuilder
from pubCode.pubEnums.flaskResEnum import ResCode
from pubCode.flaskExts.customError import *


def flashErrors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


def removeNoneKey(oriDict: dict):
    """
    移除字典中的空值
    :param oriDict:原始字典
    :return: 移除字段后的字典
    """
    assert isinstance(oriDict, dict), f"removeNoneKey参数类型错误 type(oriDict) = {type(oriDict)}"
    newDict = copy.deepcopy(oriDict)
    for k, v in oriDict.items():
        if v is None:
            newDict.pop(k)
    return newDict


def customAbort(httpStatusCode, msg=None, respData=None, **kwargs):
    """
    自定义异常处理器 免去写return 和 构造返回体 的麻烦步骤
    :param httpStatusCode: 状态码 目前支持 CustomResCode中的异常状态码 即400 500 开头的
    :param msg: 异常返回消息
    :param respData: 异常返回数据
    :return:
    """
    if respData is None:
        respData = {}
    respData.update({'origin': kwargs.get("message")})
    # 400
    if httpStatusCode == 400:
        raise ValidationError(message=msg or "请求异常!请检查链接和参数~", data=respData)
    if httpStatusCode == ResCode.NOT_FOUND:
        raise NotFoundError(message=msg or "请求的资源不存在!")
    # 500
    elif httpStatusCode == ResCode.RUNNING_ERROR:
        raise RunningError(message=msg or "运行错误!")
    elif httpStatusCode == ResCode.MISS_ARGS:
        raise MissArgsError(message=msg or "参数缺失!")
    elif httpStatusCode == ResCode.UNIQUE_ERROR:
        raise UniqueError(message=msg or "唯一性校验失败!")
    elif httpStatusCode == ResCode.NO_SUPPORT:
        raise NoSuportError(message=msg or "不支持的方式!")
    # 正常返回消息
    return abort(httpStatusCode, kwargs.get("message") or kwargs)


# 把flask_restful中的abort方法改为我们自己定义的方法
flask_restful.abort = customAbort


def paginateParams(args: dict):
    """
    从参数中取得分页参数
    :param args:
    :return:  pageNum 偏移量, limitNum 分页大小
    """
    assert isinstance(args, dict), f"paginateParams参数类型错误 type(oriDict) = {type(args)}"
    limitNum = args.pop("limit")
    pageNum = (int(args.pop("page")) - 1) * int(limitNum)
    return pageNum, limitNum

def strToJson(jsonStr: str):
    """
    将符合json格式的str对象转化为json
    因为字符串中可能存在 True/Fasle/None等 需要进行替换
    :param jsonStr:
    :return: dict
    """

    try:
        result = json.loads(
            jsonStr.replace("'", '"').replace("True", "true").replace("False", "false").replace("None", "null")
        )
    except JSONDecodeError as e:
        print(f"strToJson error {e}")
        result = jsonStr
    return result


def jsonToStr(jsonObj: (list, dict)):
    """
    将dict对象(json)中的第一层value进行dumps操作 转化为字符串 以便写入数据库
    :param jsonObj:
    :return: str json
    """
    if isinstance(jsonObj, list):
        result = []
        for i in jsonObj:
            if isinstance(i, (dict, list)):
                result.append(json.dumps(i, ensure_ascii=False))
            else:
                result.append(i)
    elif isinstance(jsonObj, dict):
        result = {}
        for k, v in jsonObj.items():
            if isinstance(v, (dict, list)):
                result[k] = json.dumps(v, ensure_ascii=False)
            else:
                result[k] = v
    else:
        raise ValueError("jsonToStr转化错误 仅支持list, dict!")
    return result


def modelToDict(modelObj: Model):
    """
    将 Model 对象转为 Dict
    :param modelObj: Model子类
    :return: Dict
    """
    if isinstance(modelObj, Model):
        modelDict = {}
        fieldList = modelObj.__dict__
        # __dict__中 _sa_instance_state是 SQLAlchemy对象属性 移除
        fieldList.pop("_sa_instance_state")
        for field in fieldList:
            modelDict.update({field: getattr(modelObj, field)})
    else:
        raise ValueError(f"modelToDict转化错误 传入的modelObj type={type(modelObj)}!")
    return modelDict


def queryParamsBuilder(args: dict, modelObj: DefaultMeta):
    """
    查询对象构造器
    :param args: 查询参数
    :param modelObj: Model子类
    :return: queryParams dict
    """
    assert isinstance(args, dict), "args 类型不合法"
    assert isinstance(modelObj, DefaultMeta), "DefaultMeta 类型不合法"
    args = removeNoneKey(args)
    queryParams = []
    for k, v in args.items():
        queryParams.append(getattr(modelObj, k).ilike(f"%{v}%"))
    return queryParams


def genUuid(prefix, length):
    """
    生成 uuid
    :param prefix: 前缀
    :param length: 总长度 因为会拼接时间和3位随机数 所以长度需要大于22
    :return: uuid str
    """
    assert isinstance(prefix, str), "prefix 类型不合法"
    assert isinstance(length, int), "length 类型不合法"
    if length - len(prefix) < 22:
        raise ValueError("冗余位数不够!")
    else:
        return prefix + arrow.now().format("YYYYMMDDHHmmssSS") + str(random.randint(100000, 999999))


if __name__ == "__main__":
    pass
