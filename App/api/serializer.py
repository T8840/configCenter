#  api 数据序列化类  包括数据的序列化与反序列化以及数据验证

import json
from marshmallow import fields

from App.api.models import Demo
from App.extensions import serialize
from App.api.models import CommonCnf, EnvCnf, SrvCnf

class JsonStr(fields.Field):
    """
    自定义Json字符串字段类
    使用Schema.load方法时, 会调用_deserialize方法, 将dict(json)转换为model类
    使用Schema.dump方法时, 会调用_serialize方法, 将符合格式的Json字符串转换为Dict
    """

    def _serialize(self, value, attr, obj):
        # print(f"_serialize befor value={repr(value)} attr={repr(attr)} obj={repr(obj)}")
        if value in ["", "null", None]:
            return {}
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            # print(f'JSONDecodeError _serialize')
            pass
        except TypeError:
            # print(f'TypeError JsonStr._serialize')
            value = {}
        #print(f"_serialize after value={repr(value)} attr={repr(attr)} obj={repr(obj)}")
        return value

    def _deserialize(self, value, attr, data):
        # print(f"_deserialize befor value={repr(value)} attr={repr(attr)} data={repr(data)}")
        if value in ["null", None]:
            return ""
        try:
            value = json.dumps(value, ensure_ascii=False)
        except json.JSONDecodeError:
            # print(f'JSONDecodeError JsonStr._deserialize')
            pass
        # print(f"_deserialize after value={repr(value)} attr={repr(attr)} data={repr(data)}")
        return value


class JsonArrayStr(fields.Field):
    """
    自定义Json 数组字符串字段类
    使用Schema.load方法时, 会调用_deserialize方法, list(json)转换为model类
    使用Schema.dump方法时, 会调用_serialize方法, 将符合格式的Json字符串转换为List
    """

    def _serialize(self, value, attr, obj):
        # print(f"_serialize befor value={repr(value)} attr={repr(attr)} obj={repr(obj)}")
        if value in ["", "null", None]:
            return []
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            # print(f'JSONDecodeError JsonArrayStr._serialize')
            pass
        # print(f"_serialize after value={repr(value)} attr={repr(attr)} obj={repr(obj)}")
        return value

    def _deserialize(self, value, attr, data):
        # print(f"_deserialize befor value={repr(value)} attr={repr(attr)} data={repr(data)}")
        if value in ["", "null", None]:
            return "[]"
        try:
            value = json.dumps(value, ensure_ascii=False)
        except json.JSONDecodeError:
            # print(f'JSONDecodeError JsonArrayStr._deserialize')
            pass
        # print(f"_deserialize after value={repr(value)} attr={repr(attr)} data={repr(data)}")
        return value


class DemoSchema(serialize.SQLAlchemyAutoSchema):

    field_1 = JsonStr()
    field_2 = JsonArrayStr()

    class Meta:
        model = Demo
        exclude = ("id", "created", "updated")


class CommonCnfSchema(serialize.SQLAlchemyAutoSchema):
    value = JsonStr()

    class Meta:
        model = CommonCnf
        exclude = ("id", "created", "updated")


class EnvCnfSchema(serialize.SQLAlchemyAutoSchema):
    value = JsonStr()

    class Meta:
        model = EnvCnf
        exclude = ("id", "created", "updated")


class SrvCnfSchema(serialize.SQLAlchemyAutoSchema):
    class Meta:
        model = SrvCnf
        exclude = ("id", "created", "updated")


class TeamProjectSchema(serialize.SQLAlchemyAutoSchema):
    class Meta:
        model = SrvCnf
        # exclude = ('id', 'created', 'updated', 'active')
        fields = ("project",)