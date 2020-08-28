#!/bin/bash
# configCenter 容器启动脚本 为了进行host注入和logs路径映射
usage()
{
    echo "使用方法:"
    echo "  run_configSrv.sh [-n container_name] [-i image_name] [-p container_port] [-h help]"
    echo "详细介绍:"
    echo "    container_name,   容器名称."
    echo "    image_name,       容器镜像的 tag 名称"
    echo "    container_port,   容器映射宿主机IP"
    echo "    help,             帮助信息"
    exit -1
}
#  默认值设定
container_name="configCenter"
container_port="6680"
while getopts "n:i:p:h" arg #选项后面的冒号表示该选项需要参数
do
    case $arg in
            n) container_name="$OPTARG";;
            i) image_name="$OPTARG";;
            p) container_port="$OPTARG";;
            h) usage;;
            ?) usage;;
    esac
done

echo "container_name=$container_name" 
echo "image_name=$image_name"
echo "container_port=$container_port"

sudo docker run -d --name $container_name \
    --add-host test1.testgroup.com:10.201.5.22 \
    \
    -e PORT=$container_port \
    -e FLASK_DEBUG=0 \
    -e FLASK_ENV=production \
    -e FLASK_APP=configCenterRun \
    -e SECRET_KEY=12345shangshandalaohu \
    -e DATABASE_URL=mysql+pymysql://testgroup:123456@10.201.5.161/configCenter \
    \
    -v /usr/testProject/configCenter/:/usr/testProject/configCenter/ \
    -v /usr/testProject/logs/configCenter/:/usr/testProject/configCenter/logs/ \
    -p $container_port:$container_port \
    $image_name
