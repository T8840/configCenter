#  api 数据库结构模型

from datetime import datetime

from App.database import Column, Model, SurrogatePK, db


class Demo(SurrogatePK, Model):
    """
    用户表
    """
    __tablename__ = "demo"
    field_1 = Column(db.String(512), nullable=False, unique=True, comment="字段1")
    field_2 = Column(db.String(512), nullable=False, unique=True, comment="字段2")
    active = Column(db.Boolean(), default=False, nullable=False, comment="是否有效")
    created = Column(db.DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated = Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 状态枚举
    ERROR = -1
    WAIT_RUN = 0
    RUNNING = 1
    SUCCEED = 2
    FAIL = 3

    # 默认倒序
    __mapper_args__ = {"order_by": created.desc()}

    def __repr__(self):
        return str(f"user_id={self.user_id} user_name={self.user_name}")



class CommonCnf(SurrogatePK, Model):
    __tablename__ = "common_cnf"
    key = Column(db.String(128), nullable=False, comment="配置key")
    value = Column(db.String(1024), nullable=False, comment="配置value")
    desc = Column(db.String(1024), nullable=True, comment="配置描述")
    active = Column(db.Boolean(), default=False, nullable=False, comment="是否有效")
    created = Column(db.DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated = Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 组合索引
    __table_args__ = (db.UniqueConstraint("key", name="uix_key"), db.Index("ix_key", "key", "created"))

    def __repr__(self):
        return f"key={self.key} value={self.value}"


class EnvCnf(SurrogatePK, Model):
    __tablename__ = "env_cnf"
    env = Column(db.String(128), nullable=False, comment="配置对应环境")
    key = Column(db.String(128), nullable=False, comment="配置key")
    value = Column(db.String(1024), nullable=False, comment="配置value")
    desc = Column(db.String(1024), nullable=True, comment="配置描述")
    active = Column(db.Boolean(), default=False, nullable=False, comment="是否有效")
    created = Column(db.DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated = Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    __table_args__ = (
        db.UniqueConstraint("env", "key", name="uix_env_key"),
        db.Index("ix_env_key", "env", "key", "created"),
    )

    def __repr__(self):
        return f"env={self.env} key={self.key} value={self.value}"


class SrvCnf(SurrogatePK, Model):
    __tablename__ = "srv_cnf"
    env = Column(db.String(128), nullable=False, comment="项目所在环境")
    team = Column(db.String(128), nullable=False, comment="项目组名称")
    project = Column(db.String(128), nullable=False, comment="项目名称")
    run_level = Column(db.Integer(), nullable=False, default=3, comment="项目运行级别")
    deploy_type = Column(db.String(128), nullable=False, comment="项目部署类型")
    current_host = Column(db.String(128), nullable=True, comment="当前部署IP地址")
    dev_master = Column(db.String(128), nullable=True, comment="开发负责人")
    test_master = Column(db.String(128), nullable=True, comment="测试负责人")
    process_key = Column(db.String(128), nullable=True, comment="进程关键词")
    desc = Column(db.String(1024), nullable=True, comment="配置描述")
    active = Column(db.Boolean(), default=False, nullable=False, comment="是否有效")
    created = Column(db.DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated = Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    __table_args__ = (
        db.UniqueConstraint("env", "team", "project", name="uix_env_team_project"),
        db.Index("ix_env_team_project", "env", "team", "project", "created"),
    )

    def __repr__(self):
        return f"env={self.env} team={self.team} project={self.project}"

