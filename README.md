# configCenter

### flask restful project


## 快速开始
1. clone项目
2. 进入项目路径
3. 执行pipenv install --dev 安装环境依赖
4. 复制并重命名环境配置文件

```
    git clone https://github.com/T8840/configCenter.git --recursive
    cd configCenter
    pipenv install --dev
    cp .env.example .env
```

## 项目结构

```

├─configCenterStatic/     # 集中静态文件目录
├──pubCode/                                # 公共代码库
│  ├─pubEnums/                             # 公共枚举类
│  └─pubUtils/                             # 公共工具类
│  └─pubExts/                              # 公共扩展类
│  └─flaskExts/                            # 公共Flask扩展类
├─logs/                                    # 日志文件路径
├─App/               # 项目主应用
│  ├─api/                                  # api域
|       ├─models.py                        # 数据结构定义
|       ├─serializer.py                    # 数据序列化转换定义
|       ├─views.py                         # 视图函数
|  ├─appFactory.py                         # App工厂方法 集中初始化及注册
|  ├─commands.py                           # 命令行注册
|  ├─database.py                           # 增强的数据库类
|  ├─extensions.py                         # 扩展管理
|  ├─settings.py                           # 项目配置
|  ├─utils.py                              # 内部工具类
|  ├─urls.py                               # url统一管理
├─requirements/                            # 依赖库文件
└─tests/                                   # 测试代码库目录
└─.env                                     # 项目本地运行时环境变量配置
└─configCenter.py         # 项目运行入口 需通过 flask run
```

## 运行项目
1. 配置环境变量 重命名.env.example --> .env (若有问题可手动设置如下)
2. 启动项目
3. 访问 `http://127.0.0.1:5000/api/hello` `http://127.0.0.1:5000/api/hello/pythoner` 验证

```
    set FLASK_APP=configCenterRun.py
    set FLASK_ENV=development
    set FLASK_DEBUG=1
    set DATABASE_URL="<YOUR DATABASE URL>"
    flask run
```


## 初始化数据库与迁移
1. 提前建立数据库
2. 不推荐使用migrate 是用手写sql和手动管理数据库
