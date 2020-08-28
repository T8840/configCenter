FROM python:3.7.2-slim-stretch
# configSrv 基础镜像

MAINTAINER T8840

# 替换sources.list
COPY sources.list /etc/apt/sources.list

# 复制当前上下文目录下 requirements.txt 文件
COPY requirements.txt ./

# 挂载 配置服务路径
VOLUME ["/usr/testProject/configCenter", "/usr/testProject/logs"]

# Flask环境参数变量
ENV FLASK_ENV production
ENV SECRET_KEY secret

# 设置时区,执行更新 通过requirements.txt 安装python库依赖
RUN mkdir /root/.pip/ \
    && /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone \
    && echo '[global]' >> /root/.pip/pip.conf \
    && echo 'trusted-host=mirrors.aliyun.com' >> /root/.pip/pip.conf \
    && echo 'index-url=https://mirrors.aliyun.com/pypi/simple/' >> /root/.pip/pip.conf \
    && pip3.7 install -r requirements.txt \
    && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/* \
	&& find /usr -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +;
# 暴露 6680 端口
EXPOSE 6680

# 指定工作目录
WORKDIR /usr/testProject/configCenter

# 执行命令启动gunicorn
CMD gunicorn configCenterRun:createApp\(\) -b 0.0.0.0:$PORT -w 4
