# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
          纸上得来终觉浅，绝知此事要躬行！
    :description:
        1.部署相关信息来自于nacos配置
            {
                "server_info": {
                    "host": "10.201.5.161",
                    "port":22,
                    "user" : "user",
                    "password": "password"
                },
                "deploy_configCenter": {
                    "project_name": "configCenter",
                    "process_name": "configCenter",
                    "container_name": "configCenter",
                    "project_deploy_path": "/usr/testProject/configCenter/",
                    "project_dev_path": "../configCenter",
                    "project_git_path": "git@github.com/configCenter.git",
                    "local_temp_path":"/deploy_temp",
                    "remote_temp_path":"/usr/testProject/deploy_temp/"
                }
            }
        2.由于远程Linux服务器与git项目处于不同网段不能直接拉取代码，故依赖于本地主机作为中转从git下拉代码打包后上传到Linux服务器
            2.1

"""

import os
import json
import arrow
import zipfile
import pathlib
import paramiko
import platform
import subprocess
import requests


def isWindows():
    return True if "Windows" in platform.system() else False

def isLinux():
    return True if "Linux" in platform.system() else False

def getInfo():
    try:
        info = requests.get("http://10.201.7.185:8848/nacos/v1/cs/configs?dataId=deploy_124&group=DEFAULT_GROUP&tenant=89362432-5255-497e-8e94-cb77d46cb1a9")
        return json.loads(info.text)
    except Exception:
        raise ConnectionRefusedError

class Deploy(object):
    def __init__(self):
        self.server_info = getInfo()["server_info"]
        self.deploy_info = getInfo()["deploy_configCenter"]
        self.projectName = "".join(
            [self.deploy_info["project_name"] if self.deploy_info["project_name"] else "projectName", arrow.now().format("MMDDHHmmss"), ".zip"]
        )
        self.backupName = "".join(
            [self.deploy_info["project_name"] if self.deploy_info["project_name"] else "projectName", arrow.now().format("MMDDHHmm"), ".bak"]
        )
        self.nowPath = pathlib.Path.cwd()
        self.sshObj = self.connectSrv()

    def connectSrv(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.server_info['host'], 22, self.server_info['user'], self.server_info['password'])
        except paramiko.SSHException as e:
            print("服务器连接失败，报错{error}".format(error=e))
        return ssh

    def runRemoteCmd(self, cmd):
        """
        执行远程命令
        :return:
        """
        print(f"runRemoteCmd执行命令 {repr(cmd)}")
        errorFlag = False
        ouput = ""
        try:
            stdin, stdout, stderr = self.sshObj.exec_command(cmd)
            ouput = stdout.readlines()
            errorMsg = stderr.readlines()
            if errorMsg:
                errorFlag = True
                ouput = errorMsg
                print("命令执行失败~")
                print(errorMsg)
        except Exception as e:
            print("命令执行异常~")
            print(e)
        return errorFlag, ouput

    def cloneProject(self, projectGitPath, tempPath):
        """从Git拉取项目到本地或远程目录"""
        subprocess.call(
            ["git", "clone", "--recurse-submodule", "--depth", "1", "-b", "master", str(projectGitPath), str(tempPath)]
        )

    def localCleaner(self, path):
        """在Windows系统清除临时文件"""
        tempPath = pathlib.Path(path).absolute()
        try:
            print(tempPath)
            os.system("rd /s/q {path}".format(path=tempPath))
        except Exception as e:
            print(e)

    def deleteFiles(self, tempPath):
        """删除git中与部署无关文件"""
        try:
            gitPath = pathlib.Path(tempPath).absolute().joinpath(pathlib.Path(".git"))
            print("删除 %s" % gitPath)
            os.system("rd /s/q {path}".format(path=gitPath))
        except Exception as e:
            print(e)

    def zipOnWin(self, tempPath):
        """在Windows系统针对git下拉的代码进行打包"""
        # 指定zip文件保存的完整路径
        fullProjectZip = pathlib.Path(tempPath).parent.joinpath(pathlib.Path(self.projectName))
        print(f"fullProjectZip = {fullProjectZip}")
        projectZip = zipfile.ZipFile(str(fullProjectZip), "w")
        # 项目目录为缓存路径 直接打包项目下文件,与FinTesterPlatform不太一样
        project = pathlib.Path(tempPath)
        print(f"project = {project}")
        with projectZip:
            for filePath in project.rglob("*"):
                # 参数1为文件完整路径 参数2为打包进zip之后的路径
                projectZip.write(
                    filePath,
                    str(filePath)
                    .replace(str(pathlib.Path(self.deploy_info['local_temp_path']).absolute()), "")
                    .replace("\\" + self.deploy_info['project_name'], ""),
                )

    def zipOnLinux(self, filePath, zipPath):
        """在Linux将原有代码进行备份打包"""
        zipCmd = f"tar -zcPf {zipPath} {filePath}"
        errFlag, ouput = self.runRemoteCmd(zipCmd)
        if not errFlag:
            print(ouput)
            print("压缩原始版本文件完成~")
        else:
            print("压缩原始版本文件失败~")
            print(ouput)

    def upload(self, localFilePath, remoteFilePath):
        """从Windows系统上传文件到Linux系统"""
        # localFilePath remoteFilePath 一定是带文件名的完整路径！！！
        srvConnect = paramiko.Transport((self.server_info['host'], 22))
        try:
            srvConnect.connect(username=self.server_info['user'], password=self.server_info['password'])
            print("连接服务器:{hostName}".format(hostName=self.server_info['host']))
            sftp = paramiko.SFTPClient.from_transport(srvConnect)
            print(
                "开始上传文件，本地完整路径:{localFilePath}\n远程完整路径:{remoteFilePath}".format(
                    localFilePath=localFilePath, remoteFilePath=remoteFilePath
                )
            )
            sftp.put(localFilePath, remoteFilePath)
            srvConnect.close()
            print("文件上传成功!")
        except ValueError as e:
            print("文件上传失败！")
            print(e)


    def remoteCleaner(self, path):
        """在Linux清除临时文件"""
        countCmd = f"cd {path} && ls -l |grep {self.deploy_info['project_name']} | wc -l"
        fileNum = 0
        errFlag, output = self.runRemoteCmd(countCmd)
        if not errFlag:
            print("执行文件统计命令成功!")
            fileNum = int(output[0])
        else:
            print(f"执行文件统计命令失败! output = {output}")
        if fileNum and fileNum >= 5:
            print(f"文件数量{fileNum} 开始清理!")
            cleanCmd = f"cd {path} && ls -lrt | grep -v 'total' | grep {self.deploy_info['project_name']} | head -n {fileNum-3} | awk '{{print$9}}' | xargs rm"
            errFlag, output = self.runRemoteCmd(cleanCmd)
            if not errFlag:
                print("执行文件清理命令成功!")
            else:
                print(f"执行文件清理命令失败! output = {output}")
        else:
            print(f"文件数量{fileNum} 跳过清理!")

    def backup(self, backupPath, originPath):
        backupName = self.deploy_info['project_name'] + "_bak" + arrow.now().format("MMDDHHmmss") + ".tar.gz"
        zipPath = backupPath + backupName
        print(f"远程备份路径为: {zipPath}")
        self.zipOnLinux(originPath, zipPath)
        return backupName

    def unzipFile(self, zipFile):
        unzipFileCmd = f"cd {self.deploy_info['remote_temp_path'] } && unzip -o {zipFile} -d {self.deploy_info['project_deploy_path']}"
        errMsg, output = self.runRemoteCmd(unzipFileCmd)
        if not errMsg:
            print("解压缩文件完成~")
        else:
            print(f"解压缩文件失败~ errMsg = {output}")

    def restartContainer(self, sshObj=None):
        """重启容器"""
        restartCmd = f"sudo docker restart {self.deploy_info['container_name']}"
        errMsg, output = self.runRemoteCmd(restartCmd)
        if not errMsg:
            print("重启项目完成~")
        else:
            print(f"重启项目失败~ errMsg = {output}")

    def doDeploy(self):
        """主流程"""
        print("自动部署开始~ \nstep0: 清理本地缓存文件")
        self.localCleaner(self.deploy_info['local_temp_path'])
        print("step1: 本地拉取gitlab最新代码~ ")
        tempPath = pathlib.Path(self.deploy_info['local_temp_path']).absolute().joinpath(pathlib.Path(self.deploy_info["project_name"]))
        print(f"缓存路径为: {tempPath}")
        self.cloneProject(self.deploy_info['project_git_path'], str(tempPath))

        print("step2: 删除一些部署无关的文件~")
        self.deleteFiles(tempPath)
        print("step3: 打包拉取到的gitlab最新代码~")
        self.zipOnWin(tempPath)
        print("step4: 远程执行代码备份")
        self.backup(self.deploy_info['remote_temp_path'], self.deploy_info['project_deploy_path'])
        print("step5: 上传代码至服务器~")
        self.upload(
            pathlib.Path(self.deploy_info['local_temp_path']).absolute().joinpath(self.projectName), self.deploy_info['remote_temp_path'] + self.projectName
        )
        print("step6: 执行部署动作")
        # 解压文件
        self.unzipFile(self.projectName)
        # 重启容器
        self.restartContainer()
        print("项目部署完成！")
        print("附加步骤 清理远程多余缓存文件！")
        self.remoteCleaner(self.deploy_info['remote_temp_path'])
        print("完成！")


if __name__ == "__main__":
    de = Deploy()
    de.doDeploy()

