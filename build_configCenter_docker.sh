#!/bin/bash
# configCenter 容器构建脚本
usage()
{
    echo "使用方法:"
    echo "  build_configCenter.sh [-p path] [-t tag_name] [-f dockerfile_name] [-h help]"
    echo "详细介绍:"
    echo "    path,            镜像编译的主目录, 约定为项目顶级目录下."
    echo "    tag_name,        镜像的 tag 名称"
    echo "    dockerfile_name, 镜像的 dockerfile 文件名"
    echo "    help,            帮助信息"
    exit -1
}
path="/usr/testProject/configCenter"
tag_name="test:configCenter_v`date +%Y%m%d%H%M`"
dockerfile_name="configCenter_v1.dockerfile"
while getopts "p:t:f:h" arg #选项后面的冒号表示该选项需要参数
do
    case $arg in
            p) path="$OPTARG";;
            t) tag_name="$OPTARG";;
            f) dockerfile_name="$OPTARG";;
            h) usage;;
            ?) usage;;
    esac
done

echo "path=$path"
echo "tag_name=$tag_name"
echo "dockerfile_name=$dockerfile_name"

cd $path \
&& sudo docker build -t $tag_name -f $dockerfile_name .
